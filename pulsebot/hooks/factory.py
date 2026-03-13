"""Build hook chains from config."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulsebot.config import HooksConfig

from pulsebot.hooks.base import ToolCallHook
from pulsebot.hooks.passthrough import PassthroughHook
from pulsebot.utils import get_logger

logger = get_logger(__name__)

_HOOK_REGISTRY: dict[str, type[ToolCallHook]] = {}


def _register_builtin_hooks() -> None:
    from pulsebot.hooks.passthrough import PassthroughHook
    from pulsebot.hooks.policy import PolicyHook
    from pulsebot.hooks.webhook import WebhookHook

    _HOOK_REGISTRY["passthrough"] = PassthroughHook
    _HOOK_REGISTRY["policy"] = PolicyHook
    _HOOK_REGISTRY["webhook"] = WebhookHook


def build_hooks(config: HooksConfig) -> list[ToolCallHook]:
    """Build a list of hooks from config.

    Returns [PassthroughHook()] if no pre_call hooks are configured.
    """
    _register_builtin_hooks()

    if not config.pre_call:
        return [PassthroughHook()]

    hooks: list[ToolCallHook] = []
    for entry in config.pre_call:
        hook_cls = _HOOK_REGISTRY.get(entry.type)
        if hook_cls is None:
            logger.warning(f"Unknown hook type '{entry.type}', skipping.")
            continue
        try:
            hook = hook_cls(**entry.config)
            hooks.append(hook)
        except Exception as exc:
            logger.error(f"Failed to build hook '{entry.type}': {exc}")
    return hooks or [PassthroughHook()]
