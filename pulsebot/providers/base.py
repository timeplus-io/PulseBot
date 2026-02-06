"""Base LLM provider interface for PulseBot."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    """Represents a tool call from the LLM."""
    
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Usage:
    """Token usage information."""
    
    input_tokens: int
    output_tokens: int
    
    @property
    def total_tokens(self) -> int:
        """Total tokens used."""
        return self.input_tokens + self.output_tokens


@dataclass
class LLMResponse:
    """Response from an LLM provider."""
    
    content: str
    tool_calls: list[ToolCall] | None = None
    usage: Usage = field(default_factory=lambda: Usage(0, 0))
    model: str = ""
    stop_reason: str = ""
    raw_response: Any = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers.
    
    All LLM providers (Anthropic, OpenAI, etc.) implement this interface
    to provide a consistent API for the agent.
    """
    
    provider_name: str
    model: str
    
    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Send a chat completion request.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system: Optional system prompt
            tools: Optional list of tool definitions (OpenAI format)
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            LLMResponse with content, tool calls, and usage info
        """
        pass
    
    def get_tool_definitions(self, tools: list[Any]) -> list[dict[str, Any]]:
        """Convert internal tool definitions to provider format.
        
        Default implementation returns OpenAI-compatible format.
        Override in subclasses if provider uses different format.
        
        Args:
            tools: List of ToolDefinition objects
            
        Returns:
            List of tool definitions in provider's format
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in tools
        ]
    
    def estimate_cost(self, usage: Usage) -> float:
        """Estimate cost based on token usage.
        
        Override with specific pricing for each provider/model.
        
        Args:
            usage: Token usage information
            
        Returns:
            Estimated cost in USD
        """
        # Default: $0 (override in subclasses with actual pricing)
        return 0.0
