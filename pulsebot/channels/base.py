"""Base channel interface for PulseBot."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ChannelMessage:
    """Normalized message from any channel."""
    
    channel: str
    user_id: str
    text: str
    session_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseChannel(ABC):
    """Base class for all channel integrations.
    
    Channels handle bidirectional communication with external platforms
    like Telegram, Slack, WhatsApp, etc.
    
    Example:
        >>> class MyChannel(BaseChannel):
        ...     name = "my_channel"
        ...     
        ...     async def start(self): ...
        ...     async def stop(self): ...
        ...     async def send_message(self, session_id, text): ...
    """
    
    name: str = "base"
    
    @abstractmethod
    async def start(self) -> None:
        """Start the channel (begin receiving messages)."""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the channel."""
        pass
    
    @abstractmethod
    async def send_message(
        self,
        session_id: str,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Send a message through the channel.
        
        Args:
            session_id: Session to send to
            text: Message text
            metadata: Channel-specific metadata
            
        Returns:
            Message ID
        """
        pass
    
    def set_message_handler(
        self,
        handler: Any,  # Callable[[ChannelMessage], Awaitable[None]]
    ) -> None:
        """Set the handler for incoming messages.
        
        Args:
            handler: Async function to process incoming messages
        """
        self._message_handler = handler
