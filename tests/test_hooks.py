"""Tests for the tool call hook system."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from pydantic import ValidationError

from pulsebot.config import HookEntryConfig, HooksConfig
from pulsebot.core.executor import ToolExecutor
from pulsebot.hooks.base import HookVerdict, ToolCallHook
from pulsebot.hooks.factory import build_hooks
from pulsebot.hooks.passthrough import PassthroughHook
from pulsebot.hooks.policy import PolicyHook
from pulsebot.hooks.webhook import WebhookHook


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


async def test_policy_deny_blocked_tool():
    hook = PolicyHook(deny_tools=["shell"])
    verdict = await hook.pre_call("shell", {"command": "ls"})
    assert verdict.verdict == "deny"
    assert "shell" in verdict.reasoning


async def test_policy_allow_listed_tool():
    hook = PolicyHook(allow_tools=["file_read"])
    verdict = await hook.pre_call("file_read", {"path": "/tmp/x"})
    assert verdict.verdict == "approve"


async def test_policy_deny_tool_not_in_allowlist():
    hook = PolicyHook(allow_tools=["file_read"])
    verdict = await hook.pre_call("shell", {"command": "ls"})
    assert verdict.verdict == "deny"


async def test_policy_deny_argument_pattern():
    hook = PolicyHook(deny_argument_patterns={"command": ["rm -rf", "sudo"]})
    verdict = await hook.pre_call("shell", {"command": "rm -rf /"})
    assert verdict.verdict == "deny"


async def test_policy_approve_safe_argument():
    hook = PolicyHook(deny_argument_patterns={"command": ["rm -rf"]})
    verdict = await hook.pre_call("shell", {"command": "ls -la"})
    assert verdict.verdict == "approve"


async def test_policy_wildcard_allow():
    hook = PolicyHook(allow_tools=["file_*"])
    v_allowed = await hook.pre_call("file_read", {})
    v_denied = await hook.pre_call("shell", {})
    assert v_allowed.verdict == "approve"
    assert v_denied.verdict == "deny"


async def test_policy_deny_takes_precedence_over_allow():
    """deny_tools always wins even if tool is in allow_tools."""
    hook = PolicyHook(allow_tools=["shell"], deny_tools=["shell"])
    verdict = await hook.pre_call("shell", {"command": "ls"})
    assert verdict.verdict == "deny"


async def test_policy_no_rules_approves_everything():
    hook = PolicyHook()
    verdict = await hook.pre_call("anything", {"x": "y"})
    assert verdict.verdict == "approve"


async def test_webhook_approves_on_200_approve():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"verdict": "approve"}

    with patch("pulsebot.hooks.webhook.httpx.AsyncClient") as mock_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_cls.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook")
        verdict = await hook.pre_call("shell", {"command": "ls"})
        assert verdict.verdict == "approve"


async def test_webhook_denies_on_deny_response():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"verdict": "deny", "reasoning": "blocked"}

    with patch("pulsebot.hooks.webhook.httpx.AsyncClient") as mock_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_cls.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook")
        verdict = await hook.pre_call("shell", {"command": "rm -rf /"})
        assert verdict.verdict == "deny"
        assert verdict.reasoning == "blocked"


async def test_webhook_approves_on_network_error_fail_open():
    with patch("pulsebot.hooks.webhook.httpx.AsyncClient") as mock_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(side_effect=httpx.RequestError("timeout", request=MagicMock()))
        mock_cls.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook", fail_open=True)
        verdict = await hook.pre_call("shell", {"command": "ls"})
        assert verdict.verdict == "approve"


async def test_webhook_denies_on_network_error_fail_closed():
    with patch("pulsebot.hooks.webhook.httpx.AsyncClient") as mock_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(side_effect=httpx.RequestError("timeout", request=MagicMock()))
        mock_cls.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook", fail_open=False)
        verdict = await hook.pre_call("shell", {"command": "ls"})
        assert verdict.verdict == "deny"


async def test_webhook_post_call_fires_and_forgets_on_error():
    """post_call should not raise even on network error."""
    with patch("pulsebot.hooks.webhook.httpx.AsyncClient") as mock_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(side_effect=Exception("connection refused"))
        mock_cls.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook")
        # Should not raise
        await hook.post_call("shell", {"command": "ls"}, {"success": True, "output": "file.txt"})


# ---------------------------------------------------------------------------
# Executor integration tests
# ---------------------------------------------------------------------------


def _make_executor(hooks=None):
    mock_loader = MagicMock()
    mock_skill = AsyncMock()
    mock_skill.execute = AsyncMock(return_value=MagicMock(
        success=True, output="ok", error=None
    ))
    mock_loader.get_skill_for_tool.return_value = mock_skill
    return ToolExecutor(mock_loader, hooks=hooks or [])


async def test_executor_passthrough_hook_approves():
    executor = _make_executor(hooks=[PassthroughHook()])
    result = await executor.execute("shell", {"command": "ls"})
    assert result["success"] is True


async def test_executor_deny_hook_blocks_execution():
    executor = _make_executor(hooks=[PolicyHook(deny_tools=["shell"])])
    result = await executor.execute("shell", {"command": "ls"})
    assert result["success"] is False
    assert "denied" in result["error"].lower()


async def test_executor_modify_hook_changes_arguments():
    class ModifyHook(ToolCallHook):
        async def pre_call(self, tool_name, arguments, session_id=""):
            return HookVerdict(verdict="modify", modified_arguments={"command": "echo safe"})
        async def post_call(self, *args, **kwargs):
            pass

    captured = {}
    mock_loader = MagicMock()
    mock_skill = AsyncMock()
    async def capture_execute(tool_name, arguments):
        captured["arguments"] = arguments
        return MagicMock(success=True, output="safe", error=None)
    mock_skill.execute = capture_execute
    mock_loader.get_skill_for_tool.return_value = mock_skill

    executor = ToolExecutor(mock_loader, hooks=[ModifyHook()])
    result = await executor.execute("shell", {"command": "rm -rf /"})
    assert result["success"] is True
    assert captured["arguments"]["command"] == "echo safe"


async def test_executor_post_hooks_run_after_execution():
    post_calls = []

    class ObserveHook(ToolCallHook):
        async def pre_call(self, tool_name, arguments, session_id=""):
            return HookVerdict(verdict="approve")
        async def post_call(self, tool_name, arguments, result, session_id=""):
            post_calls.append((tool_name, result["success"]))

    executor = _make_executor(hooks=[ObserveHook()])
    await executor.execute("shell", {"command": "ls"})
    assert post_calls == [("shell", True)]


async def test_executor_no_hooks_still_works():
    executor = _make_executor(hooks=[])
    result = await executor.execute("shell", {"command": "ls"})
    assert result["success"] is True


# ---------------------------------------------------------------------------
# Factory / config wiring tests
# ---------------------------------------------------------------------------


def test_build_hooks_empty():
    hooks = build_hooks(HooksConfig())
    # Default: one PassthroughHook
    assert len(hooks) == 1
    assert isinstance(hooks[0], PassthroughHook)


def test_build_hooks_policy():
    cfg = HooksConfig(pre_call=[
        HookEntryConfig(type="policy", config={"deny_tools": ["shell"]})
    ])
    hooks = build_hooks(cfg)
    assert len(hooks) == 1
    assert isinstance(hooks[0], PolicyHook)


def test_build_hooks_webhook():
    cfg = HooksConfig(pre_call=[
        HookEntryConfig(type="webhook", config={"url": "https://example.com/hook"})
    ])
    hooks = build_hooks(cfg)
    assert len(hooks) == 1
    assert isinstance(hooks[0], WebhookHook)
