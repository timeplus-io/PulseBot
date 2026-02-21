"""Factory functions for creating providers and other components."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulsebot.config import Config
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills import SkillLoader
    
_log = logging.getLogger(__name__)


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

    elif provider_name == "nvidia":
        from pulsebot.providers.nvidia import NvidiaProvider
        return NvidiaProvider(
            api_key=config.providers.nvidia.api_key,
            model=model,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
            timeout_seconds=config.providers.nvidia.timeout_seconds,
            enable_thinking=config.providers.nvidia.enable_thinking,
        )

    else:
        raise ValueError(f"Unknown provider: {provider_name}. Supported: anthropic, openai, openrouter, ollama, nvidia")

def create_skill_loader(config: "Config") -> "SkillLoader":
    """Create a SkillLoader with all configured builtin and custom skills.

    WorkspaceSkill is handled specially because its constructor takes a
    WorkspaceConfig object, not plain string kwargs like other builtins.
    We build the loader for everything else first, then register WorkspaceSkill
    manually with the correct argument.

    Args:
        config: Full PulseBot Config.

    Returns:
        Fully populated SkillLoader.
    """
    from pulsebot.skills import SkillLoader

    # Standard kwargs for non-workspace builtins
    skill_configs: dict = {
        "web_search": {
            "provider": config.search.provider,
            "api_key": config.search.brave_api_key,
            "searxng_url": config.search.searxng_url,
        },
    }

    # Build loader for all skills except workspace
    non_workspace = config.skills.model_copy(
        update={
            "builtin": [s for s in config.skills.builtin if s != "workspace"]
        }
    )
    loader = SkillLoader.from_config(non_workspace, **skill_configs)

    # Register WorkspaceSkill with WorkspaceConfig object
    if "workspace" in config.skills.builtin:
        from pulsebot.skills.builtin.workspace import WorkspaceSkill

        skill = WorkspaceSkill(config=config.workspace)
        loader._skills["workspace"] = skill
        for tool in skill.get_tools():
            loader._tool_to_skill[tool.name] = "workspace"

        _log.info(
            "Workspace skill registered",
            extra={"tools": [t.name for t in skill.get_tools()]},
        )

    return loader