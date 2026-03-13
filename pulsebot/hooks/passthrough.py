"""PassthroughHook — zero-overhead default that approves all tool calls."""

from __future__ import annotations

from typing import Any

from pulsebot.hooks.base import HookVerdict, ToolCallHook


class PassthroughHook(ToolCallHook):
    """Default hook: approves every tool call with no overhead."""

    async def pre_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> HookVerdict:
        """Approve the tool call unconditionally."""
        return HookVerdict(verdict="approve")

    async def post_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
        session_id: str = "",
    ) -> None:
        """No-op observer."""
