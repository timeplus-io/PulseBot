"""Telegram channel integration for PulseBot."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from pulsebot.channels.base import BaseChannel, ChannelMessage
from pulsebot.core.router import MessageRouter
from pulsebot.timeplus.streams import StreamReader, StreamWriter
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class TelegramChannel(BaseChannel):
    """Telegram bot channel integration.
    
    Receives messages from Telegram users and sends responses back.
    Uses session_id based on chat_id for conversation continuity.
    
    Example:
        >>> channel = TelegramChannel(
        ...     token="BOT_TOKEN",
        ...     timeplus_client=client,
        ... )
        >>> await channel.start()
    """
    
    name = "telegram"
    
    def __init__(
        self,
        token: str,
        timeplus_client: "TimeplusClient",
        allowed_users: list[int] | None = None,
    ):
        """Initialize Telegram channel.

        Args:
            token: Telegram bot token
            timeplus_client: Timeplus client for message routing
            allowed_users: List of allowed user IDs (None = all allowed)
        """
        from pulsebot.timeplus.client import TimeplusClient

        self.token = token
        self.tp = timeplus_client
        self.allowed_users = allowed_users

        self._app: Application | None = None

        # Create separate clients to avoid "Simultaneous queries on single connection" error
        # Reader client for streaming query (listening for responses)
        # Writer client for batch inserts (sending messages)
        writer_client = TimeplusClient(
            host=timeplus_client.host,
            port=timeplus_client.port,
            username=timeplus_client.username,
            password=timeplus_client.password,
        )
        self._writer = StreamWriter(writer_client, "messages")
        self._reader = StreamReader(timeplus_client, "messages")

        # Track chat_id -> session_id mapping
        self._sessions: dict[int, str] = {}

        logger.info("Initialized Telegram channel")
    
    async def start(self) -> None:
        """Start the Telegram bot and response listener."""
        # Build application
        self._app = Application.builder().token(self.token).build()
        
        # Register handlers
        self._app.add_handler(CommandHandler("start", self._handle_start))
        self._app.add_handler(CommandHandler("help", self._handle_help))
        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        
        # Start listening for responses (async task)
        import asyncio
        asyncio.create_task(self._listen_for_responses())
        
        # Start polling
        logger.info("Starting Telegram bot polling")
        await self._app.initialize()
        await self._app.start()
        await self._app.updater.start_polling()
    
    async def stop(self) -> None:
        """Stop the Telegram bot."""
        if self._app:
            await self._app.updater.stop()
            await self._app.stop()
            await self._app.shutdown()
            logger.info("Telegram bot stopped")
    
    async def send_message(
        self,
        session_id: str,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Send a message to a Telegram chat.
        
        Args:
            session_id: Session ID (maps to chat_id)
            text: Message text
            metadata: Optional metadata with chat_id
            
        Returns:
            Telegram message ID
        """
        metadata = metadata or {}
        chat_id = metadata.get("chat_id")
        
        # Find chat_id from session mapping
        if chat_id is None:
            for cid, sid in self._sessions.items():
                if sid == session_id:
                    chat_id = cid
                    break
        
        if chat_id is None:
            logger.warning(f"Cannot find chat_id for session: {session_id}")
            return ""
        
        if self._app:
            message = await self._app.bot.send_message(chat_id=chat_id, text=text)
            return str(message.message_id)
        return ""
    
    async def _handle_start(self, update: Update, context: Any) -> None:
        """Handle /start command."""
        if update.effective_chat:
            await update.effective_chat.send_message(
                "👋 Hello! I'm PulseBot, your AI assistant. "
                "Send me a message to get started!"
            )
    
    async def _handle_help(self, update: Update, context: Any) -> None:
        """Handle /help command."""
        if update.effective_chat:
            await update.effective_chat.send_message(
                "🤖 **PulseBot Help**\n\n"
                "Just send me a message and I'll help you with:\n"
                "- Answering questions\n"
                "- Web search\n"
                "- File operations\n"
                "- And more!\n\n"
                "Commands:\n"
                "/start - Start the bot\n"
                "/help - Show this help message"
            )
    
    async def _handle_message(self, update: Update, context: Any) -> None:
        """Handle incoming text messages."""
        if not update.effective_user or not update.effective_chat or not update.message:
            return
        
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        text = update.message.text or ""
        
        # Check if user is allowed
        if self.allowed_users and user_id not in self.allowed_users:
            await update.effective_chat.send_message(
                "Sorry, you're not authorized to use this bot."
            )
            return
        
        # Get or create session
        session_id = self._get_or_create_session(chat_id, user_id)
        
        logger.info(
            "Received Telegram message",
            extra={"chat_id": chat_id, "session_id": session_id, "length": len(text)}
        )
        
        # Route message to agent via Timeplus stream
        await self._writer.write({
            "source": "telegram",
            "target": "agent",
            "session_id": session_id,
            "message_type": "user_input",
            "content": json.dumps({"text": text}),
            "user_id": str(user_id),
            "channel_metadata": json.dumps({
                "chat_id": chat_id,
                "message_id": update.message.message_id,
                "username": update.effective_user.username,
            }),
            "priority": 0,
        })
    
    async def _listen_for_responses(self) -> None:
        """Listen for agent responses targeting this channel."""
        query = """
            SELECT * FROM messages 
            WHERE target = 'channel:telegram' 
              AND message_type = 'agent_response'
            SETTINGS seek_to='latest'
        """
        
        try:
            async for message in self._reader.stream(query):
                try:
                    session_id = message.get("session_id", "")
                    content_str = message.get("content", "{}")
                    metadata_str = message.get("channel_metadata", "{}")
                    
                    content = json.loads(content_str)
                    metadata = json.loads(metadata_str)
                    
                    text = content.get("text", "")
                    if text:
                        await self.send_message(session_id, text, metadata)
                        
                except Exception as e:
                    logger.error(f"Error sending Telegram response: {e}")
                    
        except Exception as e:
            logger.error(f"Error in Telegram response listener: {e}")
    
    def _get_or_create_session(self, chat_id: int, user_id: int) -> str:
        """Get or create session for a chat.
        
        Args:
            chat_id: Telegram chat ID
            user_id: Telegram user ID
            
        Returns:
            Session ID
        """
        if chat_id not in self._sessions:
            import uuid
            self._sessions[chat_id] = f"tg_{chat_id}_{uuid.uuid4().hex[:8]}"
        return self._sessions[chat_id]
