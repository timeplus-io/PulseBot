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
        for msg in messages:
            role = msg["role"]
            gemini_role = "user" if role in ("user", "system") else "model"
            
            parts = []
            if "content" in msg and msg["content"]:
                parts.append(types.Part.from_text(text=msg["content"]))
                
            if role == "assistant" and "tool_calls" in msg:
                # If we saved the raw Gemini Content from the original response, replay it
                # directly to preserve thought parts and their thought_signatures.
                raw_content_dict = msg.get("tool_calls", [{}])[0].get("function", {}).get("_gemini_content")
                if raw_content_dict:
                    try:
                        contents.append(types.Content.model_validate(raw_content_dict))
                        continue
                    except Exception as e:
                        logger.warning(f"Failed to replay raw Gemini content: {e}, falling back to reconstruction")

                for tc in msg.get("tool_calls", []):
                    func = tc.get("function", {})
                    args = func.get("arguments", {})
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}

                    fc = types.FunctionCall(name=func.get("name", "unknown_tool"), args=args)
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
            # Using async generate_content
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )
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
                    # Create a deterministic ID since Gemini doesn't always provide one like OpenAI does
                    call_id = f"call_{fc.name}"
                    tool_calls.append(
                        ToolCall(
                            id=call_id,
                            name=fc.name,
                            arguments=fc.args or {},
                        )
                    )

        # Store the complete raw Content for any tool-call response so that thought parts
        # (which carry thought_signature) are preserved and replayed in subsequent requests.
        if tool_calls and response.candidates:
            raw_content = response.candidates[0].content
            tool_calls[0].extra["_gemini_content"] = raw_content.model_dump(mode="json")

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
