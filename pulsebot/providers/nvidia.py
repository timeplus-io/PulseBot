"""NVIDIA API provider for PulseBot."""

from __future__ import annotations

import json
from typing import Any

import aiohttp

from pulsebot.providers.base import LLMProvider, LLMResponse, ToolCall, Usage
from pulsebot.utils import get_logger

logger = get_logger(__name__)

# NVIDIA API base URL
NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"


class NvidiaProvider(LLMProvider):
    """NVIDIA API provider for models like Kimi, Llama, etc.

    Uses NVIDIA's OpenAI-compatible API endpoint.

    Example:
        >>> provider = NvidiaProvider(
        ...     api_key="nvapi-...",
        ...     model="moonshotai/kimi-k2.5"
        ... )
        >>> response = await provider.chat(
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )
    """

    provider_name = "nvidia"

    def __init__(
        self,
        api_key: str,
        model: str = "moonshotai/kimi-k2.5",
        default_temperature: float = 0.7,
        default_max_tokens: int = 4096,
        timeout_seconds: int = 120,
        enable_thinking: bool = False,
    ):
        """Initialize NVIDIA provider.

        Args:
            api_key: NVIDIA API key (starts with nvapi-)
            model: Model to use (e.g., 'moonshotai/kimi-k2.5')
            default_temperature: Default temperature
            default_max_tokens: Default max tokens
            timeout_seconds: Request timeout
            enable_thinking: Enable thinking mode for supported models
        """
        self.api_key = api_key
        self.model = model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        self.enable_thinking = enable_thinking

        logger.info(f"Initialized NVIDIA provider: {model}")

    async def chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Send a chat completion request to NVIDIA API.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system: Optional system prompt
            tools: Optional list of tools
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Returns:
            LLMResponse with content and optional tool calls
        """
        # Build messages with system prompt
        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        # Build request payload
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": all_messages,
            "temperature": temperature or self.default_temperature,
            "max_tokens": max_tokens or self.default_max_tokens,
            "stream": False,
        }

        # Add tools if provided
        if tools:
            payload["tools"] = tools

        # Add thinking mode for supported models (like Kimi)
        if self.enable_thinking:
            payload["chat_template_kwargs"] = {"thinking": True}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{NVIDIA_API_BASE}/chat/completions",
                    headers=headers,
                    json=payload,
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"NVIDIA API error: {error_text}")
                        raise RuntimeError(f"NVIDIA request failed: HTTP {response.status}")

                    data = await response.json()

        except aiohttp.ClientError as e:
            logger.error(f"NVIDIA connection error: {e}")
            raise RuntimeError(f"Failed to connect to NVIDIA API: {e}")

        # Parse response (OpenAI-compatible format)
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})

        content = message.get("content", "")
        tool_calls = []

        if message.get("tool_calls"):
            for tc in message["tool_calls"]:
                func = tc.get("function", {})
                args = func.get("arguments", "{}")

                # Parse arguments if it's a string
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}

                tool_calls.append(
                    ToolCall(
                        id=tc.get("id", f"call_{len(tool_calls)}"),
                        name=func.get("name", ""),
                        arguments=args,
                    )
                )

        # Extract usage
        usage_data = data.get("usage", {})
        usage = Usage(
            input_tokens=usage_data.get("prompt_tokens", 0),
            output_tokens=usage_data.get("completion_tokens", 0),
        )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
            usage=usage,
            model=self.model,
            stop_reason=choice.get("finish_reason", "stop"),
            raw_response=data,
        )

    def estimate_cost(self, usage: Usage) -> float:
        """Estimate cost based on token usage.

        NVIDIA API pricing varies by model. This provides a rough estimate.

        Args:
            usage: Token usage

        Returns:
            Estimated cost in USD
        """
        # NVIDIA pricing is model-dependent, using conservative estimates
        # Adjust based on actual pricing for specific models
        input_price_per_million = 1.0  # $1 per 1M input tokens
        output_price_per_million = 3.0  # $3 per 1M output tokens

        input_cost = (usage.input_tokens / 1_000_000) * input_price_per_million
        output_cost = (usage.output_tokens / 1_000_000) * output_price_per_million

        return input_cost + output_cost
