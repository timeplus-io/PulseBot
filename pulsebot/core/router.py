"""Message router for PulseBot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.streams import StreamReader, StreamWriter

logger = get_logger(__name__)


class MessageRouter:
    """Routes messages between agents, channels, and skills.
    
    Handles:
    - Routing incoming user messages to agents
    - Routing agent responses to channels
    - Routing tool calls to skills
    - Broadcasting messages to multiple targets
    """
    
    def __init__(
        self,
        reader: "StreamReader",
        writer: "StreamWriter",
    ):
        """Initialize message router.
        
        Args:
            reader: Stream reader for messages
            writer: Stream writer for messages
        """
        self.reader = reader
        self.writer = writer
    
    async def route_to_agent(
        self,
        source: str,
        session_id: str,
        content: str,
        user_id: str = "",
        channel_metadata: str = "",
        priority: int = 0,
    ) -> str:
        """Route a message to the agent.
        
        Args:
            source: Message source (e.g., 'telegram', 'webchat')
            session_id: Session identifier
            content: JSON content string
            user_id: User identifier
            channel_metadata: Channel-specific metadata
            priority: Message priority
            
        Returns:
            Message ID
        """
        return await self.writer.write_message(
            source=source,
            target="agent",
            session_id=session_id,
            message_type="user_input",
            content=content,
            user_id=user_id,
            channel_metadata=channel_metadata,
            priority=priority,
        )
    
    async def route_to_channel(
        self,
        channel: str,
        session_id: str,
        content: str,
        user_id: str = "",
        channel_metadata: str = "",
    ) -> str:
        """Route a response to a specific channel.
        
        Args:
            channel: Target channel name
            session_id: Session identifier
            content: Response content
            user_id: User identifier
            channel_metadata: Channel-specific metadata
            
        Returns:
            Message ID
        """
        return await self.writer.write_message(
            source="agent",
            target=f"channel:{channel}",
            session_id=session_id,
            message_type="agent_response",
            content=content,
            user_id=user_id,
            channel_metadata=channel_metadata,
        )
    
    async def route_tool_call(
        self,
        session_id: str,
        tool_name: str,
        tool_call_id: str,
        arguments: str,
    ) -> str:
        """Route a tool call to be executed.
        
        Args:
            session_id: Session identifier
            tool_name: Name of the tool
            tool_call_id: Tool call ID
            arguments: JSON arguments string
            
        Returns:
            Message ID
        """
        import json
        content = json.dumps({
            "tool_name": tool_name,
            "tool_call_id": tool_call_id,
            "arguments": arguments,
        })
        
        return await self.writer.write_message(
            source="agent",
            target=f"skill:{tool_name}",
            session_id=session_id,
            message_type="tool_call",
            content=content,
        )
    
    async def route_tool_result(
        self,
        session_id: str,
        tool_call_id: str,
        result: str,
        success: bool = True,
    ) -> str:
        """Route a tool execution result.
        
        Args:
            session_id: Session identifier
            tool_call_id: Tool call ID
            result: JSON result string
            success: Whether execution succeeded
            
        Returns:
            Message ID
        """
        import json
        content = json.dumps({
            "tool_call_id": tool_call_id,
            "result": result,
            "success": success,
        })
        
        return await self.writer.write_message(
            source="skill",
            target="agent",
            session_id=session_id,
            message_type="tool_result",
            content=content,
        )
    
    async def broadcast(
        self,
        content: str,
        channels: list[str] | None = None,
        message_type: str = "broadcast",
        priority: int = 0,
    ) -> list[str]:
        """Broadcast a message to multiple channels.
        
        Args:
            content: Message content
            channels: Target channels (None = all enabled)
            message_type: Type of broadcast
            priority: Message priority
            
        Returns:
            List of message IDs
        """
        import uuid
        session_id = str(uuid.uuid4())
        
        if channels is None:
            # Default: broadcast to webchat only
            channels = ["webchat"]
        
        ids = []
        for channel in channels:
            msg_id = await self.writer.write_message(
                source="system",
                target=f"channel:{channel}",
                session_id=session_id,
                message_type=message_type,
                content=content,
                priority=priority,
            )
            ids.append(msg_id)
        
        return ids
    
    async def log_error(
        self,
        session_id: str,
        error: str,
        source: str = "agent",
    ) -> str:
        """Log an error message.
        
        Args:
            session_id: Session where error occurred
            error: Error message
            source: Error source
            
        Returns:
            Message ID
        """
        import json
        content = json.dumps({"error": error})
        
        return await self.writer.write_message(
            source=source,
            target="agent",
            session_id=session_id,
            message_type="error",
            content=content,
            priority=2,  # High priority
        )
