"""Stream reader and writer for PulseBot."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, AsyncIterator

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class StreamReader:
    """Async stream reader for real-time message consumption.
    
    Example:
        >>> reader = StreamReader(client, "messages")
        >>> async for msg in reader.stream():
        ...     print(msg)
    """
    
    def __init__(self, client: "TimeplusClient", stream_name: str):
        """Initialize stream reader.
        
        Args:
            client: Timeplus client instance
            stream_name: Name of the stream to read from
        """
        self.client = client
        self.stream_name = stream_name
    
    async def stream(
        self,
        query: str | None = None,
        seek_to: str = "latest",
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream messages from Timeplus.
        
        Args:
            query: Custom SQL query. If None, selects all from stream.
            seek_to: Starting position - 'latest', 'earliest', or timestamp
            
        Yields:
            Row dictionaries as they arrive
        """
        if query is None:
            query = f"SELECT * FROM {self.stream_name} SETTINGS seek_to='{seek_to}'"
        
        logger.info(
            "Starting stream",
            extra={"stream": self.stream_name, "seek_to": seek_to}
        )
        
        async for row in self.client.stream_query(query):
            yield row
    
    def read_history(
        self,
        session_id: str | None = None,
        limit: int = 100,
        since: datetime | None = None,
        message_types: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Read historical messages (batch query).
        
        Args:
            session_id: Filter by session ID
            limit: Maximum number of messages to return
            since: Only return messages after this time
            message_types: Filter by message types
            
        Returns:
            List of message dictionaries, newest first
        """
        conditions = []
        
        if session_id:
            conditions.append(f"session_id = '{session_id}'")
        if since:
            conditions.append(f"timestamp >= '{since.isoformat()}'")
        if message_types:
            types_str = ", ".join(f"'{t}'" for t in message_types)
            conditions.append(f"message_type IN ({types_str})")
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        query = f"""
            SELECT * FROM table({self.stream_name})
            {where_clause}
            ORDER BY timestamp DESC
            LIMIT {limit}
        """
        
        return self.client.query(query)
    
    def get_conversation(
        self,
        session_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get conversation history for a session.
        
        Args:
            session_id: Session ID to retrieve
            limit: Maximum messages to return
            
        Returns:
            List of messages in chronological order
        """
        messages = self.read_history(
            session_id=session_id,
            limit=limit,
            message_types=["user_input", "agent_response", "tool_call", "tool_result"],
        )
        # Reverse to get chronological order
        return list(reversed(messages))


class StreamWriter:
    """Stream writer for publishing messages.
    
    Example:
        >>> writer = StreamWriter(client, "messages")
        >>> await writer.write({"content": "Hello", "source": "agent"})
    """
    
    def __init__(self, client: "TimeplusClient", stream_name: str):
        """Initialize stream writer.
        
        Args:
            client: Timeplus client instance
            stream_name: Name of the stream to write to
        """
        self.client = client
        self.stream_name = stream_name
    
    async def write(self, data: dict[str, Any]) -> str:
        """Write a single message to the stream.
        
        Automatically sets id and timestamp if not provided.
        
        Args:
            data: Message data dictionary
            
        Returns:
            The message ID
        """
        # Ensure required fields have defaults
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        if "timestamp" not in data:
            data["timestamp"] = datetime.now(timezone.utc)
        
        self.client.insert(self.stream_name, [data])
        
        logger.debug(
            "Wrote message",
            extra={"stream": self.stream_name, "id": data["id"]}
        )
        
        return data["id"]
    
    async def write_batch(self, data: list[dict[str, Any]]) -> list[str]:
        """Write multiple messages efficiently.
        
        Args:
            data: List of message dictionaries
            
        Returns:
            List of message IDs
        """
        ids = []
        for item in data:
            if "id" not in item:
                item["id"] = str(uuid.uuid4())
            if "timestamp" not in item:
                item["timestamp"] = datetime.now(timezone.utc)
            ids.append(item["id"])
        
        self.client.insert(self.stream_name, data)
        
        logger.debug(
            "Wrote batch",
            extra={"stream": self.stream_name, "count": len(data)}
        )
        
        return ids
    
    async def write_message(
        self,
        source: str,
        target: str,
        session_id: str,
        message_type: str,
        content: str,
        user_id: str = "",
        channel_metadata: str = "",
        priority: int = 0,
    ) -> str:
        """Write a structured message with all standard fields.
        
        Args:
            source: Message source (e.g., 'agent', 'telegram')
            target: Message target (e.g., 'agent', 'channel:telegram')
            session_id: Session identifier
            message_type: Type of message (e.g., 'user_input', 'agent_response')
            content: JSON content string
            user_id: User identifier
            channel_metadata: Channel-specific metadata JSON
            priority: Message priority (-1 to 2)
            
        Returns:
            Message ID
        """
        return await self.write({
            "source": source,
            "target": target,
            "session_id": session_id,
            "message_type": message_type,
            "content": content,
            "user_id": user_id,
            "channel_metadata": channel_metadata,
            "priority": priority,
        })
