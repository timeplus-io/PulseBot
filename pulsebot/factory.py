"""Factory functions for creating providers and other components."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulsebot.config import Config
    from pulsebot.providers.base import LLMProvider


def create_provider(config: "Config") -> "LLMProvider":
    """Create an LLM provider based on configuration.
    
    Args:
        config: PulseBot configuration
        
    Returns:
        Configured LLM provider instance
    """
    provider_name = config.agent.provider.lower()
    model = config.agent.model
    
    if provider_name == "anthropic":
        from pulsebot.providers.anthropic import AnthropicProvider
        return AnthropicProvider(
            api_key=config.providers.anthropic.api_key,
            model=model,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
        )
    
    elif provider_name == "openai":
        from pulsebot.providers.openai import OpenAIProvider
        return OpenAIProvider(
            api_key=config.providers.openai.api_key,
            model=model,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
        )
    
    elif provider_name == "openrouter":
        from pulsebot.providers.openai import OpenAIProvider
        return OpenAIProvider(
            api_key=config.providers.openrouter.api_key,
            base_url="https://openrouter.ai/api/v1",
            model=model,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
        )
    
    elif provider_name == "ollama":
        from pulsebot.providers.ollama import OllamaProvider
        return OllamaProvider(
            host=config.providers.ollama.host,
            model=model,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
            timeout_seconds=config.providers.ollama.timeout_seconds,
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider_name}. Supported: anthropic, openai, openrouter, ollama")
