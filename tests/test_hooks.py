"""Tests for the tool call hook system."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from pulsebot.hooks.base import HookVerdict, ToolCallHook
from pulsebot.hooks.passthrough import PassthroughHook


def test_hook_verdict_approve():
    v = HookVerdict(verdict="approve")
    assert v.verdict == "approve"
    assert v.modified_arguments is None
    assert v.reasoning is None


def test_hook_verdict_deny():
    v = HookVerdict(verdict="deny", reasoning="not allowed")
    assert v.verdict == "deny"
    assert v.reasoning == "not allowed"


def test_hook_verdict_modify():
    v = HookVerdict(verdict="modify", modified_arguments={"cmd": "ls"})
    assert v.verdict == "modify"
    assert v.modified_arguments == {"cmd": "ls"}


def test_hook_verdict_invalid():
    with pytest.raises(ValidationError):
        HookVerdict(verdict="unknown")


def test_hook_verdict_modify_without_arguments_raises():
    """Verify that verdict='modify' without modified_arguments raises ValidationError."""
    with pytest.raises(ValidationError):
        HookVerdict(verdict="modify")


class ConcreteHook(ToolCallHook):
    """Minimal concrete implementation of ToolCallHook used in tests."""

    async def pre_call(self, tool_name: str, arguments: dict, session_id: str = "") -> HookVerdict:
        """Approve every tool call unconditionally."""
        return HookVerdict(verdict="approve")

    async def post_call(self, tool_name: str, arguments: dict, result: dict, session_id: str = "") -> None:
        """No-op post-call observer."""


def test_hook_base_instantiation():
    hook = ConcreteHook()
    assert hook is not None


async def test_hook_setup_is_noop():
    hook = ConcreteHook()
    await hook.setup()  # Must not raise


async def test_hook_teardown_is_noop():
    hook = ConcreteHook()
    await hook.teardown()  # Must not raise


async def test_passthrough_approves_everything():
    hook = PassthroughHook()
    verdict = await hook.pre_call("shell", {"command": "ls"})
    assert verdict.verdict == "approve"
    assert verdict.modified_arguments is None
    assert verdict.reasoning is None


async def test_passthrough_post_call_is_noop():
    hook = PassthroughHook()
    # Should not raise
    await hook.post_call("shell", {"command": "ls"}, {"success": True, "output": "file.txt"})


async def test_passthrough_approves_any_tool():
    hook = PassthroughHook()
    for tool in ["shell", "file_read", "web_search", "unknown_tool"]:
        verdict = await hook.pre_call(tool, {})
        assert verdict.verdict == "approve"
