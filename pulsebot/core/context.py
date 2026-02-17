"""Context builder for assembling prompt context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pulsebot.core.prompts import build_system_prompt
from pulsebot.utils import get_logger, safe_json_dumps, truncate_string

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.memory import MemoryManager

logger = get_logger(__name__)


@dataclass
class Context:
    """Assembled context for LLM prompt."""

    system_prompt: str
    messages: list[dict[str, Any]]
    tools: list[Any] = field(default_factory=list)
    memories: list[dict[str, Any]] = field(default_factory=list)
    session_id: str = ""
    user_id: str = ""
    channel: str = "webchat"

    def add_tool_result(self, tool_call_id: str, result: Any) -> None:
        """Add a tool result to the message history.

        Args:
            tool_call_id: ID of the tool call
            result: Result from tool execution
        """
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": safe_json_dumps(result) if not isinstance(result, str) else result,
        })

    def add_assistant_message(self, content: str, tool_calls: list[dict] | None = None) -> None:
        """Add an assistant message to the history.

        Args:
            content: Message content
            tool_calls: Optional tool calls
        """
        msg = {"role": "assistant", "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.messages.append(msg)


class ContextBuilder:
    """Build context for LLM prompts from conversation history and memory.

    Assembles:
    - System prompt with agent identity, tools, and memories
    - Conversation history from Timeplus messages stream
    - Relevant memories via vector search

    Example:
        >>> builder = ContextBuilder(timeplus_client, memory_manager)
        >>> context = await builder.build(
        ...     session_id="abc123",
        ...     user_message="What's the weather?",
        ... )
    """

    def __init__(
        self,
        timeplus_client: "TimeplusClient",
        memory_manager: "MemoryManager | None" = None,
        agent_name: str = "PulseBot",
        custom_identity: str = "",
        custom_instructions: str = "",
        model_info: str = "",
        skills_index: str = "",
    ):
        """Initialize context builder.

        Args:
            timeplus_client: Timeplus client for fetching history
            memory_manager: Optional memory manager for semantic search
            agent_name: Agent display name
            custom_identity: Custom persona description
            custom_instructions: Additional instructions
            skills_index: Formatted agentskills.io skill index for prompt
        """
        self.timeplus = timeplus_client
        self.memory = memory_manager
        self.agent_name = agent_name
        self.custom_identity = custom_identity
        self.custom_instructions = custom_instructions
        self.model_info = model_info
        self.skills_index = skills_index

    async def build(
        self,
        session_id: str,
        user_message: str,
        tools: list[Any] | None = None,
        include_memory: bool = True,
        memory_limit: int = 10,
        history_limit: int = 20,
        user_name: str = "User",
        channel: str = "webchat",
    ) -> Context:
        """Build complete context for LLM prompt.

        Args:
            session_id: Session identifier
            user_message: Current user message
            tools: Available tools
            include_memory: Whether to include memory search
            memory_limit: Max memories to retrieve
            history_limit: Max history messages to include
            user_name: User display name
            channel: Channel name

        Returns:
            Assembled Context object
        """
        tools = tools or []

        # Fetch conversation history
        history = await self._get_conversation_history(session_id, history_limit)
        
        logger.debug(
            "Fetched conversation history",
            extra={
                "session_id": session_id,
                "history_count": len(history),
                "history_preview": [
                    {
                        "type": h.get("message_type", ""),
                        "content_preview": truncate_string(h.get("content", ""), 100)
                    }
                    for h in history[-3:]  # Last 3 messages
                ] if history else []
            }
        )

        # Fetch relevant memories (only if embedding provider is configured)
        memories = []
        if include_memory and self.memory and user_message and self.memory.is_available():
            memories = await self._get_relevant_memories(user_message, memory_limit)

        # Build system prompt
        system_prompt = build_system_prompt(
            agent_name=self.agent_name,
            tools=tools,
            memories=memories,
            user_name=user_name,
            session_id=session_id,
            channel_name=channel,
            custom_identity=self.custom_identity,
            custom_instructions=self.custom_instructions,
            model_info=self.model_info,
            skills_index=self.skills_index,
        )

        # Build messages list
        messages = self._format_history(history)

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message,
        })

        logger.debug(
            "Built context",
            extra={
                "session_id": session_id,
                "history_count": len(history),
                "memory_count": len(memories),
                "tool_count": len(tools),
            }
        )

        return Context(
            system_prompt=system_prompt,
            messages=messages,
            tools=tools,
            memories=memories,
            session_id=session_id,
            channel=channel,
        )

    async def _get_conversation_history(
        self,
        session_id: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Fetch conversation history from Timeplus.

        Args:
            session_id: Session to fetch
            limit: Max messages

        Returns:
            List of message dicts in chronological order
        """
        try:
            query = f"""
            SELECT * FROM table(messages)
            WHERE session_id = '{session_id}'
            AND message_type IN ('user_input', 'agent_response', 'tool_call', 'tool_result')
            ORDER BY timestamp DESC
            LIMIT {limit}
            """
            result = self.timeplus.query(query)
            # Reverse to get chronological order
            return list(reversed(result))
        except Exception as e:
            logger.warning(f"Failed to fetch history: {e}")
            return []

    async def _get_relevant_memories(
        self,
        query: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Fetch relevant memories via vector search.

        Args:
            query: Search query
            limit: Max results

        Returns:
            List of memory dicts
        """
        logger.info(
            "Searching for relevant memories",
            extra={"query": truncate_string(query, 100), "limit": limit}
        )

        try:
            memories = await self.memory.search(query, limit=limit)

            memory_count = len(memories)
            if memory_count > 0:
                logger.info(f"Found {memory_count} relevant memories")
                logger.debug(
                    "Relevant memories",
                    extra={
                        "memories": [
                            {
                                "type": m.get("memory_type", "fact"),
                                "content": truncate_string(m.get("content", ""), 100),
                                "score": m.get("score", 0),
                            }
                            for m in memories
                        ]
                    }
                )
            else:
                logger.info("No relevant memories found")

            return memories
        except Exception as e:
            logger.error(f"Failed to fetch memories: {e}")
            return []

    def _format_history(self, history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Format Timeplus messages as LLM conversation.

        Args:
            history: Raw messages from Timeplus

        Returns:
            Formatted message list
        """
        messages = []

        for msg in history:
            msg_type = msg.get("message_type", "")
            content = msg.get("content", "")

            # Parse JSON content if needed
            try:
                import json
                parsed = json.loads(content) if content else {}
                text = parsed.get("text", content)
            except (json.JSONDecodeError, TypeError):
                text = content

            if msg_type == "user_input":
                messages.append({"role": "user", "content": text})
            elif msg_type == "agent_response":
                messages.append({"role": "assistant", "content": text})
            elif msg_type == "tool_call":
                # Tool calls are part of assistant messages
                pass
            elif msg_type == "tool_result":
                # Tool results use tool role
                messages.append({
                    "role": "tool",
                    "tool_call_id": msg.get("id", ""),
                    "content": text,
                })

        return messages
