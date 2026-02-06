"""Anthropic Claude provider for PulseBot."""

from __future__ import annotations

import json
from typing import Any

import anthropic

from pulsebot.providers.base import LLMProvider, LLMResponse, ToolCall, Usage
from pulsebot.utils import get_logger

logger = get_logger(__name__)

# Pricing per 1M tokens (as of 2024)
ANTHROPIC_PRICING = {
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
}


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider implementation.
    
    Example:
        >>> provider = AnthropicProvider(api_key="...")
        >>> response = await provider.chat(
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )
    """
    
    provider_name = "anthropic"
    
    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        default_temperature: float = 0.7,
        default_max_tokens: int = 4096,
    ):
        """Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key
            model: Model to use
            default_temperature: Default temperature
            default_max_tokens: Default max tokens
        """
        self.model = model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        
        self.client = anthropic.Anthropic(api_key=api_key)
        
        logger.info(f"Initialized Anthropic provider with model: {model}")
    
    async def chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Send a chat completion request to Claude.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system: Optional system prompt
            tools: Optional list of tools in OpenAI format
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            LLMResponse with content and tool calls
        """
        # Convert messages to Anthropic format
        anthropic_messages = self._convert_messages(messages)
        
        # Build request
        request = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens or self.default_max_tokens,
            "temperature": temperature or self.default_temperature,
        }
        
        if system:
            request["system"] = system
        
        if tools:
            request["tools"] = self._convert_tools(tools)
        
        # Make request
        try:
            response = self.client.messages.create(**request)
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise
        
        # Parse response
        content = ""
        tool_calls = []
        
        for block in response.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input,
                    )
                )
        
        usage = Usage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
        
        return LLMResponse(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
            usage=usage,
            model=self.model,
            stop_reason=response.stop_reason or "",
            raw_response=response,
        )
    
    def _convert_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Convert OpenAI-style messages to Anthropic format.
        
        Handles tool results specially as Anthropic expects them in a specific format.
        """
        result = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Handle assistant messages with tool calls
            if role == "assistant" and msg.get("tool_calls"):
                content_blocks = []
                if content:
                    content_blocks.append({"type": "text", "text": content})
                
                for tc in msg["tool_calls"]:
                    content_blocks.append({
                        "type": "tool_use",
                        "id": tc.get("id", ""),
                        "name": tc.get("function", {}).get("name", ""),
                        "input": json.loads(tc.get("function", {}).get("arguments", "{}")),
                    })
                
                result.append({"role": "assistant", "content": content_blocks})
            
            # Handle tool results
            elif role == "tool":
                result.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg.get("tool_call_id", ""),
                        "content": content,
                    }],
                })
            
            # Handle regular messages
            else:
                # Map 'system' role to 'user' (system handled separately)
                if role == "system":
                    continue
                result.append({"role": role, "content": content})
        
        return result
    
    def _convert_tools(self, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Convert OpenAI tool format to Anthropic format."""
        anthropic_tools = []
        
        for tool in tools:
            if tool.get("type") == "function":
                func = tool.get("function", {})
                anthropic_tools.append({
                    "name": func.get("name", ""),
                    "description": func.get("description", ""),
                    "input_schema": func.get("parameters", {}),
                })
        
        return anthropic_tools
    
    def estimate_cost(self, usage: Usage) -> float:
        """Estimate cost based on token usage.
        
        Args:
            usage: Token usage
            
        Returns:
            Estimated cost in USD
        """
        pricing = ANTHROPIC_PRICING.get(self.model, {"input": 3.0, "output": 15.0})
        
        input_cost = (usage.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (usage.output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost
