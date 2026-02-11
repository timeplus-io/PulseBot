"""Ollama provider for local LLM inference."""

from __future__ import annotations

import json
from typing import Any

import aiohttp

from pulsebot.providers.base import LLMProvider, LLMResponse, ToolCall, Usage
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class OllamaProvider(LLMProvider):
    """Ollama provider for local LLM inference.
    
    Uses Ollama's OpenAI-compatible API endpoint.
    
    Example:
        >>> provider = OllamaProvider(model="llama3")
        >>> response = await provider.chat(
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )
        
        # With custom host
        >>> provider = OllamaProvider(
        ...     host="http://localhost:11434",
        ...     model="codellama:13b"
        ... )
    """
    
    provider_name = "ollama"
    
    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "llama3",
        default_temperature: float = 0.7,
        default_max_tokens: int = 4096,
        timeout_seconds: int = 120,
    ):
        """Initialize Ollama provider.
        
        Args:
            host: Ollama server URL
            model: Model name (e.g., 'llama3', 'mistral', 'codellama')
            default_temperature: Default temperature
            default_max_tokens: Default max tokens
            timeout_seconds: Request timeout
        """
        self.host = host.rstrip("/")
        self.model = model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        
        logger.info(f"Initialized Ollama provider: {host} model={model}")
    
    async def chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Send a chat completion request to Ollama.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system: Optional system prompt
            tools: Optional list of tools (limited support in Ollama)
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            LLMResponse with content
        """
        # Build messages with system prompt
        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})

        # Preprocess messages for Ollama compatibility
        for msg in messages:
            processed_msg = {"role": msg["role"], "content": msg.get("content", "")}

            # Handle tool calls in assistant messages
            if msg.get("tool_calls"):
                processed_msg["tool_calls"] = []
                for tc in msg["tool_calls"]:
                    func = tc.get("function", {})
                    args = func.get("arguments", {})
                    # Ensure arguments is a dict, not a JSON string
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                    processed_msg["tool_calls"].append({
                        "function": {
                            "name": func.get("name", ""),
                            "arguments": args,
                        }
                    })

            # Handle tool result messages
            if msg["role"] == "tool":
                # Ollama expects tool results in a specific format
                processed_msg["content"] = msg.get("content", "")

            all_messages.append(processed_msg)
        
        # Debug the final messages
        logger.debug(
            "Final messages being sent to Ollama",
            extra={
                "model": self.model,
                "message_count": len(all_messages),
                "messages_preview": [
                    {
                        "role": msg.get("role", ""),
                        "content_preview": (msg.get("content", "")[:100] if msg.get("content") else "Empty")
                    }
                    for msg in all_messages[-2:]  # Last 2 messages
                ]
            }
        )

        # Build request payload
        payload = {
            "model": self.model,
            "messages": all_messages,
            "stream": False,
            "options": {
                "temperature": temperature or self.default_temperature,
                "num_predict": max_tokens or self.default_max_tokens,
            },
        }

        # Add tools if provided (Ollama has limited tool support)
        if tools:
            payload["tools"] = tools
        
        # Debug logging
        logger.debug(
            "Ollama request",
            extra={
                "host": self.host,
                "model": self.model,
                "message_count": len(all_messages),
                "payload_preview": {
                    "model": payload["model"],
                    "message_sample": payload["messages"][-1] if payload["messages"] else {},
                    "options": payload["options"]
                }
            }
        )
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.host}/api/chat",
                    json=payload,
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ollama error: {error_text}")
                        raise RuntimeError(f"Ollama request failed: HTTP {response.status}")
                    
                    data = await response.json()
                    
                    # Debug response
                    logger.debug(
                        "Ollama response",
                        extra={
                            "host": self.host,
                            "model": self.model,
                            "status": response.status,
                            "response_keys": list(data.keys()) if isinstance(data, dict) else "Not dict",
                            "response_sample": str(data)[:500]
                        }
                    )
        
        except aiohttp.ClientError as e:
            logger.error(f"Ollama connection error: {e}")
            raise RuntimeError(f"Failed to connect to Ollama at {self.host}: {e}")
        
        # Parse response
        message = data.get("message", {})
        content = message.get("content", "")
        
        # Some models (like Kimi) use "thinking" field for processing results
        # If content is empty but thinking field has content, use that
        thinking_content = message.get("thinking", "")
        if not content and thinking_content:
            logger.debug(
                "Using thinking field for content (model may use separate processing field)",
                extra={
                    "model": self.model,
                    "thinking_content_preview": thinking_content[:100]
                }
            )
            content = thinking_content
        
        # Some models might return content in different fields
        if not content:
            # Check response field (some models use this)
            content = data.get("response", "")
        
        # Debug logging for model responses
        logger.debug(
            "Ollama model response parsing",
            extra={
                "model": self.model,
                "data_keys": list(data.keys()) if isinstance(data, dict) else "Not dict",
                "message_keys": list(message.keys()) if isinstance(message, dict) else "Not dict",
                "content_field": content[:100] if content else "Empty",
                "message_content_field": message.get("content", "Missing")[:100] if isinstance(message.get("content"), str) else "Not string",
                "message_thinking_field": message.get("thinking", "Missing")[:100] if isinstance(message.get("thinking"), str) else "Not string",
                "response_field": data.get("response", "Missing")[:100] if isinstance(data.get("response"), str) else "Not string",
                "raw_response_sample": str(data)[:300]
            }
        )
        
        # Parse tool calls if present
        tool_calls = []
        if message.get("tool_calls"):
            for tc in message["tool_calls"]:
                func = tc.get("function", {})
                tool_calls.append(
                    ToolCall(
                        id=tc.get("id", f"call_{len(tool_calls)}"),
                        name=func.get("name", ""),
                        arguments=func.get("arguments", {}),
                    )
                )
        
        # Extract usage (Ollama provides different metrics)
        eval_count = data.get("eval_count", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)
        
        usage = Usage(
            input_tokens=prompt_eval_count,
            output_tokens=eval_count,
        )
        
        return LLMResponse(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
            usage=usage,
            model=self.model,
            stop_reason=data.get("done_reason", "stop"),
            raw_response=data,
        )
    
    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Simple text generation (non-chat interface).
        
        Args:
            prompt: Text prompt
            system: Optional system prompt
            temperature: Optional temperature
            max_tokens: Optional max tokens
            
        Returns:
            Generated text
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature or self.default_temperature,
                "num_predict": max_tokens or self.default_max_tokens,
            },
        }
        
        if system:
            payload["system"] = system
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.host}/api/generate",
                json=payload,
            ) as response:
                if response.status != 200:
                    raise RuntimeError(f"Ollama request failed: HTTP {response.status}")
                
                data = await response.json()
                return data.get("response", "")
    
    async def list_models(self) -> list[dict[str, Any]]:
        """List available models on the Ollama server.
        
        Returns:
            List of model info dicts
        """
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(f"{self.host}/api/tags") as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                return data.get("models", [])
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry.
        
        Args:
            model_name: Model to pull (e.g., 'llama3', 'mistral')
            
        Returns:
            True if successful
        """
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=600)) as session:
            async with session.post(
                f"{self.host}/api/pull",
                json={"name": model_name, "stream": False},
            ) as response:
                return response.status == 200
    
    def estimate_cost(self, usage: Usage) -> float:
        """Ollama is free/local - always returns 0.
        
        Args:
            usage: Token usage (ignored)
            
        Returns:
            0.0 (local inference has no per-token cost)
        """
        return 0.0
