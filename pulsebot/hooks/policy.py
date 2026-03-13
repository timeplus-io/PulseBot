"""PolicyHook — allow/deny tool calls by name and argument patterns."""

from __future__ import annotations

import fnmatch
import re
from typing import Any

from pulsebot.hooks.base import HookVerdict, ToolCallHook


class PolicyHook(ToolCallHook):
    """Evaluates tool calls against configurable allow/deny rules.

    Rules are evaluated in this order:
    1. If tool name matches any deny_tools pattern → deny
    2. If any argument value matches a deny_argument_patterns regex → deny
    3. If allow_tools is set and tool name does NOT match any pattern → deny
    4. Otherwise → approve

    Args:
        allow_tools: Whitelist of tool name patterns (fnmatch). If set, only
            matching tools are approved. Supports wildcards, e.g. ``"file_*"``.
        deny_tools: Blacklist of tool name patterns (fnmatch). Takes precedence.
        deny_argument_patterns: Map of argument key → list of regex patterns.
            If any argument value matches, the call is denied.
    """

    def __init__(
        self,
        allow_tools: list[str] | None = None,
        deny_tools: list[str] | None = None,
        deny_argument_patterns: dict[str, list[str]] | None = None,
    ) -> None:
        self._allow_tools = allow_tools or []
        self._deny_tools = deny_tools or []
        self._deny_arg_patterns = deny_argument_patterns or {}

    def _matches_any(self, name: str, patterns: list[str]) -> bool:
        """Return True if name matches any fnmatch pattern in the list."""
        return any(fnmatch.fnmatch(name, p) for p in patterns)

    async def pre_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> HookVerdict:
        """Evaluate the tool call against the configured policy rules."""
        # Deny list takes precedence
        if self._deny_tools and self._matches_any(tool_name, self._deny_tools):
            return HookVerdict(
                verdict="deny",
                reasoning=f"Tool '{tool_name}' is in the deny list.",
            )

        # Argument pattern checks
        for arg_key, patterns in self._deny_arg_patterns.items():
            value = str(arguments.get(arg_key, ""))
            for pattern in patterns:
                if re.search(pattern, value):
                    return HookVerdict(
                        verdict="deny",
                        reasoning=(
                            f"Argument '{arg_key}' matches denied pattern '{pattern}'."
                        ),
                    )

        # Allow list: if set, only listed tools are approved
        if self._allow_tools and not self._matches_any(tool_name, self._allow_tools):
            return HookVerdict(
                verdict="deny",
                reasoning=f"Tool '{tool_name}' is not in the allow list.",
            )

        return HookVerdict(verdict="approve")

    async def post_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
        session_id: str = "",
    ) -> None:
        """No-op observer."""
