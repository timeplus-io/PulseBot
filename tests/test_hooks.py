"""Tests for the tool call hook system."""

import pytest
from pydantic import ValidationError

from pulsebot.hooks.base import HookVerdict, ToolCallHook


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


class ConcreteHook(ToolCallHook):
    async def pre_call(self, tool_name, arguments, session_id=""):
        return HookVerdict(verdict="approve")
    async def post_call(self, tool_name, arguments, result, session_id=""):
        pass


def test_hook_base_instantiation():
    hook = ConcreteHook()
    assert hook is not None
