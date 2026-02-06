"""OpenAI provider for PulseBot."""

from __future__ import annotations

import json
from typing import Any

import openai

from pulsebot.providers.base import LLMProvider, LLMResponse, ToolCall, Usage
from pulsebot.utils import get_logger

logger = get_logger(__name__)

# Pricing per 1M tokens (as of 2024)
OPENAI_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
}


class OpenAIProvider(LLMProvider):
    """OpenAI ChatGPT/GPT-4 provider implementation.
    
    Also supports OpenRouter by specifying a custom base URL.
    
    Example:
        >>> provider = OpenAIProvider(api_key="...")
        >>> response = await provider.chat(
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )
        
        # For OpenRouter:
        >>> provider = OpenAIProvider(
        ...     api_key="...",
        ...     base_url="https://openrouter.ai/api/v1",
        ...     model="anthropic/claude-sonnet-4-20250514"
        ... )
    """
    
    provider_name = "openai"
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str | None = None,
        default_temperature: float = 0.7,
        default_max_tokens: int = 4096,
    ):
        """Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: Model to use
            base_url: Optional base URL (for OpenRouter compatibility)
            default_temperature: Default temperature
            default_max_tokens: Default max tokens
        """
        self.model = model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
            self.provider_name = "openrouter"
        
        self.client = openai.OpenAI(**client_kwargs)
        
        logger.info(
            f"Initialized OpenAI provider with model: {model}",
            extra={"base_url": base_url}
        )
    
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
            messages: List of message dicts
            system: Optional system prompt
            tools: Optional list of tools
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            LLMResponse with content and tool calls
        """
        # Build messages with system prompt if provided
        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)
        
        # Build request
        request = {
            "model": self.model,
            "messages": all_messages,
            "temperature": temperature or self.default_temperature,
            "max_tokens": max_tokens or self.default_max_tokens,
        }
        
        if tools:
            request["tools"] = tools
        
        # Make request
        try:
            response = self.client.chat.completions.create(**request)
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        
        # Parse response
        choice = response.choices[0]
        message = choice.message
        
        content = message.content or ""
        tool_calls = []
        
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    arguments = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}
                
                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=arguments,
                    )
                )
        
        usage = Usage(
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
        )
        
        return LLMResponse(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
            usage=usage,
            model=self.model,
            stop_reason=choice.finish_reason or "",
            raw_response=response,
        )
    
    def estimate_cost(self, usage: Usage) -> float:
        """Estimate cost based on token usage.
        
        Args:
            usage: Token usage
            
        Returns:
            Estimated cost in USD
        """
        # Try model-specific pricing, fall back to gpt-4o
        pricing = OPENAI_PRICING.get(self.model, OPENAI_PRICING.get("gpt-4o", {"input": 2.5, "output": 10.0}))
        
        input_cost = (usage.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (usage.output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost
