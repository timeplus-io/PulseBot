"""Gemini provider for PulseBot."""

from __future__ import annotations

import json
from typing import Any

from pulsebot.providers.base import LLMProvider, LLMResponse, ToolCall, Usage
from pulsebot.utils import get_logger

logger = get_logger(__name__)

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


class GeminiProvider(LLMProvider):
    """Google Gemini provider implementation (using new google-genai SDK).
    
    Example:
        >>> provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
        >>> response = await provider.chat(
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )
    """
    
    provider_name = "gemini"
    
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        default_temperature: float = 0.7,
        default_max_tokens: int = 4096,
    ):
        """Initialize Gemini provider.
        
        Args:
            api_key: Gemini API key
            model: Model to use (e.g. gemini-2.5-flash, gemini-2.5-pro)
            default_temperature: Default temperature
            default_max_tokens: Default max tokens
        """
        if not HAS_GENAI:
            raise ImportError(
                "google-genai is not installed. "
                "Please install it with: pip install google-genai"
            )
            
        self.model = model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.client = genai.Client(api_key=api_key)
        
        logger.info(f"Initialized Gemini provider with model: {model}")

    def get_tool_definitions(self, tools: list[Any]) -> list[dict[str, Any]]:
        """Convert internal tool definitions to Gemini format.
        
        Args:
            tools: List of internal ToolDefinition objects
            
        Returns:
            List of Gemini tools
        """
        gemini_tools = []
        for tool in tools:
            # We map JSON Schema Types to Gemini's expected types 
            # Note: The new SDK generally accepts standard JSON Schema dicts for function declarations
            desc = {"name": tool.name, "description": tool.description}
            if tool.parameters:
                desc["parameters"] = tool.parameters
            gemini_tools.append({"function_declarations": [desc]})
            
        return gemini_tools
    
    async def chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Send a chat completion request to Gemini."""
        
        # Determine generation config
        config = types.GenerateContentConfig(
            temperature=temperature if temperature is not None else self.default_temperature,
            max_output_tokens=max_tokens or self.default_max_tokens,
            system_instruction=system,
        )
        
        if tools:
            config.tools = tools
            
        # Convert messages from PulseBot format ({role, content/tool_calls}) to Gemini types.Content
        contents = []
        # Carry the latest thought_signature forward across all messages in this request.
        # Gemini thinking models may produce multiple assistant messages with tool_calls (one
        # per tool call), but only the first stores _thought_signature.  All subsequent
        # function_call Parts still need it, so we propagate the last seen value.
        latest_thought_sig: bytes | None = None

        for msg in messages:
            role = msg["role"]
            gemini_role = "user" if role in ("user", "system") else "model"

            parts = []
            if "content" in msg and msg["content"]:
                parts.append(types.Part.from_text(text=msg["content"]))

            if role == "assistant" and "tool_calls" in msg:
                # Prefer the per-message thought_signature; fall back to carry-forward value.
                msg_thought_sig: bytes | None = (
                    msg.get("tool_calls", [{}])[0].get("function", {}).get("_thought_signature")
                )
                if msg_thought_sig:
                    latest_thought_sig = msg_thought_sig  # update carry-forward
                effective_sig = msg_thought_sig or latest_thought_sig

                if effective_sig:
                    source = "" if msg_thought_sig else " (carried forward)"
                    logger.info(
                        f"Replaying function_call Parts with thought_signature"
                        f" (len={len(effective_sig)}){source}"
                    )
                else:
                    logger.info("No thought_signature for function_call Parts")

                for tc in msg.get("tool_calls", []):
                    func = tc.get("function", {})
                    args = func.get("arguments", {})
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}

                    fc = types.FunctionCall(name=func.get("name", "unknown_tool"), args=args)
                    if effective_sig:
                        parts.append(types.Part(function_call=fc, thought_signature=effective_sig))
                    else:
                        parts.append(types.Part(function_call=fc))
                    
            if role == "tool" and "tool_call_id" in msg:
                content_val = msg.get("content", "Success")
                # tool_call_id is set to "call_{tool_name}" — extract the actual name
                tool_call_id = msg["tool_call_id"]
                tool_name = tool_call_id[len("call_"):] if tool_call_id.startswith("call_") else tool_call_id
                parts.append(types.Part.from_function_response(
                    name=tool_name,
                    response={"result": content_val}
                ))
                
            contents.append(types.Content(role=gemini_role, parts=parts))

        try:
            # Using async generate_content with a timeout so rate-limit retries
            # inside the SDK don't hang indefinitely.
            import asyncio
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                ),
                timeout=120.0,
            )
        except asyncio.TimeoutError:
            logger.error("Gemini API call timed out after 120s")
            raise TimeoutError("Gemini API call timed out after 120s")
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
            
        # Parse Response
        content_text = ""
        tool_calls = []
        
        if response.parts:
            for part in response.parts:
                # Skip thought parts in text content (they're model-internal reasoning)
                if part.text and not part.thought:
                    content_text += part.text
                if part.function_call:
                    fc = part.function_call
                    # Gemini thinking models (e.g. gemini-3-pro-preview) prefix tool names
                    # with a namespace like "default_api:" — strip it for the executor
                    # but keep the original name in the call_id so from_function_response
                    # sends back the matching namespaced name the model expects.
                    fc_name = fc.name or "unknown_tool"
                    executor_name = fc_name.split(":", 1)[-1] if ":" in fc_name else fc_name
                    call_id = f"call_{fc_name}"
                    tool_calls.append(
                        ToolCall(
                            id=call_id,
                            name=executor_name,
                            arguments=fc.args or {},
                        )
                    )

        # Extract and store thought_signature bytes for use in subsequent requests.
        # Gemini thinking models return thought_signature on thought Parts; the API
        # requires it on function_call Parts in the next turn.  Store as raw bytes
        # to avoid base64 encoding/decoding complexity.
        if tool_calls and response.candidates:
            raw_content = response.candidates[0].content
            if raw_content:
                thought_sig: bytes | None = None
                for part in (raw_content.parts or []):
                    if part.thought_signature:
                        thought_sig = part.thought_signature
                        break
                if thought_sig:
                    logger.info(f"Storing thought_signature (len={len(thought_sig)}) for next turn")
                    tool_calls[0].extra["_thought_signature"] = thought_sig
                else:
                    logger.info("No thought_signature in response parts (non-thinking model?)")

        # Map Usage
        usage = Usage(0, 0)
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            meta = response.usage_metadata
            usage = Usage(
                input_tokens=meta.prompt_token_count or 0,
                output_tokens=meta.candidates_token_count or 0,
            )
            
        return LLMResponse(
            content=content_text,
            tool_calls=tool_calls if tool_calls else None,
            usage=usage,
            model=self.model,
            stop_reason=response.candidates[0].finish_reason.name if response.candidates else "",
            raw_response=response,
        )

    def estimate_cost(self, usage: Usage) -> float:
        """Estimate cost based on token usage.
        
        Prices for gemini-2.5-flash: $0.075 / 1M input, $0.30 / 1M output
        Prices for gemini-2.5-pro: $1.25 / 1M input, $5.00 / 1M output
        """
        pricing = {"input": 0.0, "output": 0.0}
        if "flash" in self.model:
            pricing = {"input": 0.075, "output": 0.30}
        elif "pro" in self.model:
            pricing = {"input": 1.25, "output": 5.00}
            
        input_cost = (usage.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (usage.output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
