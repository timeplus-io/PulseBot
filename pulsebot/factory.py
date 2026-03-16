"""Factory functions for creating providers and other components."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulsebot.config import Config
    from pulsebot.core.executor import ToolExecutor
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
        openai_cfg = config.providers.openai
        return OpenAIProvider(
            api_key=openai_cfg.api_key,
            model=model,
            base_url=openai_cfg.base_url,
            provider_name=openai_cfg.provider_name,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
        )
    
    elif provider_name == "openrouter":
        from pulsebot.providers.openai import OpenAIProvider
        openrouter_cfg = config.providers.openrouter
        return OpenAIProvider(
            api_key=openrouter_cfg.api_key,
            base_url=openrouter_cfg.base_url or "https://openrouter.ai/api/v1",
            model=model,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
            provider_name=openrouter_cfg.provider_name or "openrouter",
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

    elif provider_name == "gemini":
        from pulsebot.providers.gemini import GeminiProvider
        return GeminiProvider(
            api_key=config.providers.gemini.api_key,
            model=model,
            default_temperature=config.agent.temperature,
            default_max_tokens=config.agent.max_tokens,
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
        raise ValueError(
            f"Unknown provider: {provider_name}. "
            f"Supported: anthropic, openai, openrouter, ollama, nvidia, gemini. "
            f"For OpenAI-compatible vendors (e.g. Alibaba Qwen, DeepSeek), set "
            f"agent.provider to 'openai' and configure providers.openai.base_url."
        )

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
    skill_configs: dict = {}

    # Build loader for all skills except those that need special construction
    _SPECIAL = {"workspace", "scheduler", "skill_manager"}
    non_workspace = config.skills.model_copy(
        update={
            "builtin": [s for s in config.skills.builtin if s not in _SPECIAL]
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

    # Register SchedulerSkill with timeplus_config and api_url
    if "scheduler" in config.skills.builtin:
        from pulsebot.skills.builtin.scheduler import SchedulerSkill

        api_url = config.workspace.api_server_url
        skill = SchedulerSkill(timeplus_config=config.timeplus, api_url=api_url)
        loader._skills["scheduler"] = skill
        for tool in skill.get_tools():
            loader._tool_to_skill[tool.name] = "scheduler"

        _log.info(
            "Scheduler skill registered",
            extra={"tools": [t.name for t in skill.get_tools()]},
        )

    # Register SkillManagerSkill with skills config + a dedicated Timeplus client
    if "skill_manager" in config.skills.builtin:
        from pulsebot.skills.builtin.skill_manager import SkillManagerSkill
        from pulsebot.timeplus.client import TimeplusClient

        skill = SkillManagerSkill(
            skills_config=config.skills,
            client=TimeplusClient.from_config(config.timeplus),
            loader=loader,
        )
        loader._skills["skill_manager"] = skill
        for tool in skill.get_tools():
            loader._tool_to_skill[tool.name] = "skill_manager"

        _log.info(
            "SkillManager skill registered",
            extra={"tools": [t.name for t in skill.get_tools()]},
        )

    return loader


def create_executor(config: "Config", skill_loader: "SkillLoader") -> "ToolExecutor":
    """Create a ToolExecutor with hooks from config."""
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.hooks.factory import build_hooks

    hooks = build_hooks(config.hooks.tool_call)
    return ToolExecutor(skill_loader, hooks=hooks)
