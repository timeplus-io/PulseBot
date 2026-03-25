# Tool Call Hooks Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a pre/post hook system to `ToolExecutor` so tool calls can be approved, denied, or modified before execution, with results observable after.

**Architecture:** A new `pulsebot/hooks/` package defines an abstract `ToolCallHook` base class with `pre_call()` → `HookVerdict` and `post_call()` (observability-only). `ToolExecutor` accepts a list of hooks, runs them in sequence before/after `skill.execute()`, and short-circuits on `deny`. Built-in hooks: `PassthroughHook` (default, zero cost), `PolicyHook` (allow/deny regex rules), `WebhookHook` (HTTP callback), `HumanApprovalHook` (stream-based pause).

**Tech Stack:** Python 3.11+, pydantic, httpx (already a dep), Timeplus events stream (existing `StreamWriter`).

---

## Background: Key Files

- `pulsebot/core/executor.py` — `ToolExecutor.execute()`: the single chokepoint; hooks go here
- `pulsebot/core/agent.py:128` — creates `ToolExecutor(skill_loader)`; will pass hooks
- `pulsebot/config.py` — pydantic config models; add `HooksConfig` / `HookConfig`
- `pulsebot/factory.py` — `create_skill_loader()`; also build hooks and pass to executor
- `pulsebot/skills/base.py` — `ToolResult` model (for reference in hooks)
- `tests/` — existing test files for reference patterns

---

## Task 1: Base Classes (`pulsebot/hooks/base.py`)

**Files:**
- Create: `pulsebot/hooks/__init__.py`
- Create: `pulsebot/hooks/base.py`
- Test: `tests/test_hooks.py`

**Step 1: Write the failing test**

```python
# tests/test_hooks.py
import pytest
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
    with pytest.raises(Exception):
        HookVerdict(verdict="unknown")


class ConcreteHook(ToolCallHook):
    async def pre_call(self, tool_name, arguments, session_id=""):
        return HookVerdict(verdict="approve")
    async def post_call(self, tool_name, arguments, result, session_id=""):
        pass


def test_hook_base_instantiation():
    hook = ConcreteHook()
    assert hook is not None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_hooks.py -v
```
Expected: FAIL with `ModuleNotFoundError: No module named 'pulsebot.hooks'`

**Step 3: Write `pulsebot/hooks/__init__.py`**

```python
"""Tool call hook system for PulseBot."""

from pulsebot.hooks.base import HookVerdict, ToolCallHook

__all__ = ["HookVerdict", "ToolCallHook"]
```

**Step 4: Write `pulsebot/hooks/base.py`**

```python
"""Base classes for the tool call hook system."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Literal

from pydantic import BaseModel


class HookVerdict(BaseModel):
    """Result from a pre-call hook."""

    verdict: Literal["approve", "deny", "modify"]
    modified_arguments: dict[str, Any] | None = None
    reasoning: str | None = None


class ToolCallHook(ABC):
    """Abstract base for pre/post tool call hooks.

    Implement ``pre_call`` to intercept tool calls before execution.
    Implement ``post_call`` for observability after execution.
    """

    async def setup(self) -> None:
        """Optional lifecycle: called once when the hook is initialized."""

    async def teardown(self) -> None:
        """Optional lifecycle: called once when the agent shuts down."""

    @abstractmethod
    async def pre_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> HookVerdict:
        """Inspect/approve/deny/modify a tool call before execution.

        Returns:
            HookVerdict with verdict "approve", "deny", or "modify".
            For "modify", set ``modified_arguments`` to the replacement dict.
        """

    @abstractmethod
    async def post_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
        session_id: str = "",
    ) -> None:
        """Observe a tool call result after execution (no return value)."""
```

**Step 5: Run tests to verify they pass**

```bash
pytest tests/test_hooks.py -v
```
Expected: 5 tests PASS.

**Step 6: Commit**

```bash
git add pulsebot/hooks/__init__.py pulsebot/hooks/base.py tests/test_hooks.py
git commit -m "feat: add ToolCallHook base classes and HookVerdict model"
```

---

## Task 2: PassthroughHook (`pulsebot/hooks/passthrough.py`)

**Files:**
- Create: `pulsebot/hooks/passthrough.py`
- Test: `tests/test_hooks.py` (append)

**Step 1: Add tests**

```python
# Append to tests/test_hooks.py
import pytest
from pulsebot.hooks.passthrough import PassthroughHook


@pytest.mark.asyncio
async def test_passthrough_approves_everything():
    hook = PassthroughHook()
    verdict = await hook.pre_call("shell", {"command": "ls"})
    assert verdict.verdict == "approve"


@pytest.mark.asyncio
async def test_passthrough_post_call_is_noop():
    hook = PassthroughHook()
    # Should not raise
    await hook.post_call("shell", {"command": "ls"}, {"success": True, "output": "file.txt"})
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_hooks.py::test_passthrough_approves_everything -v
```
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write `pulsebot/hooks/passthrough.py`**

```python
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
        return HookVerdict(verdict="approve")

    async def post_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
        session_id: str = "",
    ) -> None:
        pass
```

Update `pulsebot/hooks/__init__.py`:

```python
"""Tool call hook system for PulseBot."""

from pulsebot.hooks.base import HookVerdict, ToolCallHook
from pulsebot.hooks.passthrough import PassthroughHook

__all__ = ["HookVerdict", "ToolCallHook", "PassthroughHook"]
```

**Step 4: Run tests**

```bash
pytest tests/test_hooks.py -v
```
Expected: All PASS.

**Step 5: Commit**

```bash
git add pulsebot/hooks/passthrough.py pulsebot/hooks/__init__.py tests/test_hooks.py
git commit -m "feat: add PassthroughHook (zero-overhead default)"
```

---

## Task 3: PolicyHook (`pulsebot/hooks/policy.py`)

Evaluates tool calls against allow/deny lists with regex pattern matching.
Rules checked in order: if a deny pattern matches → deny; if an allow list is set and no pattern matches → deny; otherwise → approve.

**Files:**
- Create: `pulsebot/hooks/policy.py`
- Test: `tests/test_hooks.py` (append)

**Step 1: Add tests**

```python
# Append to tests/test_hooks.py
import pytest
from pulsebot.hooks.policy import PolicyHook


@pytest.mark.asyncio
async def test_policy_deny_blocked_tool():
    hook = PolicyHook(deny_tools=["shell"])
    verdict = await hook.pre_call("shell", {"command": "ls"})
    assert verdict.verdict == "deny"
    assert "shell" in verdict.reasoning


@pytest.mark.asyncio
async def test_policy_allow_listed_tool():
    hook = PolicyHook(allow_tools=["file_read"])
    verdict = await hook.pre_call("file_read", {"path": "/tmp/x"})
    assert verdict.verdict == "approve"


@pytest.mark.asyncio
async def test_policy_deny_tool_not_in_allowlist():
    hook = PolicyHook(allow_tools=["file_read"])
    verdict = await hook.pre_call("shell", {"command": "ls"})
    assert verdict.verdict == "deny"


@pytest.mark.asyncio
async def test_policy_deny_argument_pattern():
    hook = PolicyHook(deny_argument_patterns={"command": ["rm -rf", "sudo"]})
    verdict = await hook.pre_call("shell", {"command": "rm -rf /"})
    assert verdict.verdict == "deny"


@pytest.mark.asyncio
async def test_policy_approve_safe_argument():
    hook = PolicyHook(deny_argument_patterns={"command": ["rm -rf"]})
    verdict = await hook.pre_call("shell", {"command": "ls -la"})
    assert verdict.verdict == "approve"


@pytest.mark.asyncio
async def test_policy_wildcard_allow():
    hook = PolicyHook(allow_tools=["file_*"])
    v_allowed = await hook.pre_call("file_read", {})
    v_denied = await hook.pre_call("shell", {})
    assert v_allowed.verdict == "approve"
    assert v_denied.verdict == "deny"
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_hooks.py -k "policy" -v
```
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write `pulsebot/hooks/policy.py`**

```python
"""PolicyHook — allow/deny tool calls by name and argument patterns."""

from __future__ import annotations

import fnmatch
import re
from typing import Any

from pulsebot.hooks.base import HookVerdict, ToolCallHook


class PolicyHook(ToolCallHook):
    """Evaluates tool calls against configurable allow/deny rules.

    Args:
        allow_tools: Whitelist of tool name patterns (fnmatch). If set, only
            listed tools are approved. Supports wildcards, e.g. ``"file_*"``.
        deny_tools: Blacklist of tool name patterns. Takes precedence over allow.
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
        return any(fnmatch.fnmatch(name, p) for p in patterns)

    async def pre_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> HookVerdict:
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
        pass
```

Update `pulsebot/hooks/__init__.py` to export `PolicyHook`.

**Step 4: Run tests**

```bash
pytest tests/test_hooks.py -v
```
Expected: All PASS.

**Step 5: Commit**

```bash
git add pulsebot/hooks/policy.py pulsebot/hooks/__init__.py tests/test_hooks.py
git commit -m "feat: add PolicyHook with allow/deny rules and argument pattern matching"
```

---

## Task 4: WebhookHook (`pulsebot/hooks/webhook.py`)

POSTs tool call info to an external HTTP endpoint; approves/denies based on response.

**Files:**
- Create: `pulsebot/hooks/webhook.py`
- Test: `tests/test_hooks.py` (append)

**Step 1: Add tests**

```python
# Append to tests/test_hooks.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pulsebot.hooks.webhook import WebhookHook


@pytest.mark.asyncio
async def test_webhook_approves_on_200_approve():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"verdict": "approve"}

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook")
        verdict = await hook.pre_call("shell", {"command": "ls"})
        assert verdict.verdict == "approve"


@pytest.mark.asyncio
async def test_webhook_denies_on_200_deny():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"verdict": "deny", "reasoning": "blocked"}

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook")
        verdict = await hook.pre_call("shell", {"command": "rm -rf /"})
        assert verdict.verdict == "deny"
        assert verdict.reasoning == "blocked"


@pytest.mark.asyncio
async def test_webhook_approves_on_request_error():
    """Webhook failures should default to approve (fail-open)."""
    import httpx
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(side_effect=httpx.RequestError("timeout"))
        mock_client_class.return_value = mock_client

        hook = WebhookHook(url="https://example.com/hook", fail_open=True)
        verdict = await hook.pre_call("shell", {"command": "ls"})
        assert verdict.verdict == "approve"
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_hooks.py -k "webhook" -v
```
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write `pulsebot/hooks/webhook.py`**

```python
"""WebhookHook — POST tool call info to an external HTTP endpoint."""

from __future__ import annotations

from typing import Any

import httpx

from pulsebot.hooks.base import HookVerdict, ToolCallHook
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class WebhookHook(ToolCallHook):
    """Sends pre-call information to an external HTTP endpoint.

    The endpoint should respond with JSON: ``{"verdict": "approve"|"deny"|"modify",
    "reasoning": "...", "modified_arguments": {...}}``.

    Args:
        url: HTTPS endpoint to POST to.
        auth_header: Optional ``Authorization`` header value.
        timeout: Request timeout in seconds (default 5).
        fail_open: If True (default), approve on network/timeout errors.
            If False, deny on errors (fail-closed / safer).
    """

    def __init__(
        self,
        url: str,
        auth_header: str | None = None,
        timeout: float = 5.0,
        fail_open: bool = True,
    ) -> None:
        self._url = url
        self._headers = {"Content-Type": "application/json"}
        if auth_header:
            self._headers["Authorization"] = auth_header
        self._timeout = timeout
        self._fail_open = fail_open

    async def pre_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> HookVerdict:
        payload = {
            "tool_name": tool_name,
            "arguments": arguments,
            "session_id": session_id,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._url,
                    json=payload,
                    headers=self._headers,
                    timeout=self._timeout,
                )
                data = response.json()
                verdict = data.get("verdict", "approve")
                if verdict not in ("approve", "deny", "modify"):
                    verdict = "approve"
                return HookVerdict(
                    verdict=verdict,
                    reasoning=data.get("reasoning"),
                    modified_arguments=data.get("modified_arguments"),
                )
        except Exception as exc:
            logger.warning(
                "WebhookHook request failed",
                extra={"url": self._url, "error": str(exc)},
            )
            if self._fail_open:
                return HookVerdict(verdict="approve", reasoning=f"Webhook failed: {exc}")
            return HookVerdict(verdict="deny", reasoning=f"Webhook failed (fail-closed): {exc}")

    async def post_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
        session_id: str = "",
    ) -> None:
        payload = {
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "session_id": session_id,
        }
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    self._url,
                    json={"event": "post_call", **payload},
                    headers=self._headers,
                    timeout=self._timeout,
                )
        except Exception as exc:
            logger.warning(
                "WebhookHook post_call failed",
                extra={"url": self._url, "error": str(exc)},
            )
```

Update `pulsebot/hooks/__init__.py` to export `WebhookHook`.

**Step 4: Run tests**

```bash
pytest tests/test_hooks.py -v
```
Expected: All PASS.

**Step 5: Commit**

```bash
git add pulsebot/hooks/webhook.py pulsebot/hooks/__init__.py tests/test_hooks.py
git commit -m "feat: add WebhookHook for external HTTP policy callbacks"
```

---

## Task 5: Wire Hooks into `ToolExecutor`

Hooks run in sequence. Pre-call: first `deny` short-circuits the chain. Post-call: all hooks run regardless.

**Files:**
- Modify: `pulsebot/core/executor.py`
- Test: `tests/test_hooks.py` (append)

**Step 1: Add tests**

```python
# Append to tests/test_hooks.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from pulsebot.core.executor import ToolExecutor
from pulsebot.hooks.base import HookVerdict
from pulsebot.hooks.passthrough import PassthroughHook
from pulsebot.hooks.policy import PolicyHook


def _make_executor(hooks=None):
    mock_loader = MagicMock()
    mock_skill = AsyncMock()
    mock_skill.execute = AsyncMock(return_value=MagicMock(
        success=True, output="ok", error=None
    ))
    mock_loader.get_skill_for_tool.return_value = mock_skill
    return ToolExecutor(mock_loader, hooks=hooks or [])


@pytest.mark.asyncio
async def test_executor_passthrough_hook_approves():
    executor = _make_executor(hooks=[PassthroughHook()])
    result = await executor.execute("shell", {"command": "ls"})
    assert result["success"] is True


@pytest.mark.asyncio
async def test_executor_deny_hook_blocks_execution():
    executor = _make_executor(hooks=[PolicyHook(deny_tools=["shell"])])
    result = await executor.execute("shell", {"command": "ls"})
    assert result["success"] is False
    assert "denied" in result["error"].lower()


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_executor_no_hooks_still_works():
    executor = _make_executor(hooks=[])
    result = await executor.execute("shell", {"command": "ls"})
    assert result["success"] is True
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_hooks.py -k "executor" -v
```
Expected: FAIL — `ToolExecutor.__init__` doesn't accept `hooks` yet.

**Step 3: Modify `pulsebot/core/executor.py`**

Change `__init__` signature and add hook execution to `execute()`:

```python
# pulsebot/core/executor.py — modified sections

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.hooks.base import ToolCallHook
    from pulsebot.skills.loader import SkillLoader

logger = get_logger(__name__)


class ToolExecutor:
    def __init__(
        self,
        skill_loader: "SkillLoader",
        hooks: "list[ToolCallHook] | None" = None,
    ):
        self.skills = skill_loader
        self._hooks: list[ToolCallHook] = hooks or []
        self._execution_count = 0

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> dict[str, Any]:
        self._execution_count += 1

        logger.info(
            "Executing tool",
            extra={
                "tool": tool_name,
                "session_id": session_id,
                "execution_id": self._execution_count,
            },
        )

        try:
            if not tool_name:
                inferred_name = self._infer_tool_from_args(arguments)
                if inferred_name:
                    logger.warning(
                        "Inferred empty tool name from arguments",
                        extra={"inferred_tool": inferred_name, "arguments": arguments},
                    )
                    tool_name = inferred_name
                else:
                    return {
                        "success": False,
                        "output": None,
                        "error": "Invalid tool call: tool name is empty and could not be inferred.",
                    }

            # Find the skill
            skill = self.skills.get_skill_for_tool(tool_name)
            if skill is None:
                return {
                    "success": False,
                    "output": None,
                    "error": f"Unknown tool: {tool_name}",
                }

            # --- Pre-call hooks ---
            effective_arguments = arguments
            for hook in self._hooks:
                verdict = await hook.pre_call(tool_name, effective_arguments, session_id)
                if verdict.verdict == "deny":
                    logger.info(
                        "Tool call denied by hook",
                        extra={
                            "tool": tool_name,
                            "hook": type(hook).__name__,
                            "reasoning": verdict.reasoning,
                        },
                    )
                    return {
                        "success": False,
                        "output": None,
                        "error": (
                            f"Tool call denied by {type(hook).__name__}: "
                            f"{verdict.reasoning or 'no reason given'}"
                        ),
                    }
                if verdict.verdict == "modify" and verdict.modified_arguments is not None:
                    effective_arguments = verdict.modified_arguments

            # --- Execute ---
            result = await skill.execute(tool_name, effective_arguments)

            logger.info(
                "Tool execution complete",
                extra={
                    "tool": tool_name,
                    "success": result.success,
                    "execution_id": self._execution_count,
                },
            )

            result_dict = {
                "success": result.success,
                "output": result.output,
                "error": result.error,
            }

            # --- Post-call hooks (all run, errors are logged not raised) ---
            for hook in self._hooks:
                try:
                    await hook.post_call(tool_name, effective_arguments, result_dict, session_id)
                except Exception as exc:
                    logger.warning(
                        "Post-call hook error (ignored)",
                        extra={"hook": type(hook).__name__, "error": str(exc)},
                    )

            return result_dict

        except Exception as e:
            logger.error(
                "Tool execution failed",
                extra={
                    "tool": tool_name,
                    "error": str(e),
                    "execution_id": self._execution_count,
                },
            )
            return {
                "success": False,
                "output": None,
                "error": str(e),
            }

    # ... rest of the methods unchanged (execute_batch, get_tool_definitions, _infer_tool_from_args)
```

**Step 4: Run tests**

```bash
pytest tests/test_hooks.py -v
```
Expected: All PASS.

**Step 5: Commit**

```bash
git add pulsebot/core/executor.py tests/test_hooks.py
git commit -m "feat: integrate pre/post hooks into ToolExecutor"
```

---

## Task 6: Config Models + Factory Wiring

Add `HookConfig` / `HooksConfig` to `pulsebot/config.py` and wire hooks in `factory.py`.

**Files:**
- Modify: `pulsebot/config.py`
- Modify: `pulsebot/factory.py`
- Test: `tests/test_hooks.py` (append)

**Step 1: Add tests**

```python
# Append to tests/test_hooks.py
from pulsebot.hooks.passthrough import PassthroughHook
from pulsebot.hooks.policy import PolicyHook
from pulsebot.hooks.webhook import WebhookHook
from pulsebot.hooks.factory import build_hooks
from pulsebot.config import HookEntryConfig, HooksConfig


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
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_hooks.py -k "build_hooks" -v
```
Expected: FAIL with `ImportError`

**Step 3: Add config models to `pulsebot/config.py`**

Add after `SkillsConfig` (around line 134):

```python
class HookEntryConfig(BaseModel):
    """Configuration for a single hook in the chain."""
    type: str  # "passthrough", "policy", "webhook"
    config: dict[str, Any] = Field(default_factory=dict)


class HooksConfig(BaseModel):
    """Tool call hooks configuration."""
    pre_call: list[HookEntryConfig] = Field(default_factory=list)
    # post_call hooks share the same chain; hooks that implement post_call will fire
```

Add `hooks: HooksConfig` to the `Config` class:

```python
class Config(BaseSettings):
    ...
    hooks: HooksConfig = Field(default_factory=HooksConfig)
```

**Step 4: Create `pulsebot/hooks/factory.py`**

```python
"""Build hook chains from config."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

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


def build_hooks(config: "HooksConfig") -> list[ToolCallHook]:
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
```

**Step 5: Wire into `pulsebot/factory.py`**

In `create_skill_loader()`, after `loader = SkillLoader.from_config(...)`:

```python
# Build tool call hooks
from pulsebot.hooks.factory import build_hooks
hooks = build_hooks(config.hooks)
```

Then pass to the executor — but `ToolExecutor` is created in `Agent.__init__` (line 128), not here.

Instead, add a new factory function `create_executor()` (or pass `hooks` to `Agent`):

Add to `pulsebot/factory.py`:

```python
def create_executor(config: "Config", skill_loader: "SkillLoader") -> "ToolExecutor":
    """Create a ToolExecutor with hooks from config."""
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.hooks.factory import build_hooks

    hooks = build_hooks(config.hooks)
    return ToolExecutor(skill_loader, hooks=hooks)
```

Then in `pulsebot/core/agent.py`, modify `__init__` to accept an optional pre-built executor:

```python
# pulsebot/core/agent.py — change line 128
# Before:
self.executor = ToolExecutor(skill_loader)

# After:
self.executor = executor if executor is not None else ToolExecutor(skill_loader)
```

Add `executor: "ToolExecutor | None" = None` to `Agent.__init__` parameters.

Update the CLI run command in `pulsebot/cli.py` to use `create_executor`:

```python
# In the run command, after create_skill_loader:
from pulsebot.factory import create_executor
executor = create_executor(cfg, skill_loader)
# Pass to Agent:
agent = Agent(..., executor=executor)
```

**Step 6: Run all tests**

```bash
pytest tests/ -v
```
Expected: All PASS.

**Step 7: Commit**

```bash
git add pulsebot/config.py pulsebot/hooks/factory.py pulsebot/factory.py pulsebot/core/agent.py pulsebot/cli.py tests/test_hooks.py
git commit -m "feat: add HooksConfig, build_hooks factory, wire into Agent"
```

---

## Task 7: Update `config.yaml` template + docs

**Files:**
- Modify: `pulsebot/config.py` (the `generate_default_config` function)

**Step 1: Add hooks section to `generate_default_config()` in `pulsebot/config.py`**

Append to the default config YAML string (after the `workspace:` section):

```yaml
# Tool call hooks — intercept tool calls before/after execution
# hooks:
#   pre_call:
#     - type: passthrough        # Default: approve everything (< 0.1ms overhead)
#
#     # Example: block specific tools
#     - type: policy
#       config:
#         deny_tools: ["shell"]
#         allow_tools: ["file_read", "file_write"]
#
#     # Example: external approval endpoint
#     - type: webhook
#       config:
#         url: "https://your-approval-service.example.com/hook"
#         auth_header: "Bearer ${WEBHOOK_SECRET}"
#         timeout: 5.0
#         fail_open: true    # approve on network error (false = deny on error)
```

**Step 2: Run tests**

```bash
pytest tests/ -v
```
Expected: All PASS.

**Step 3: Commit**

```bash
git add pulsebot/config.py
git commit -m "docs: add hooks section to default config template"
```

---

## Final Verification

```bash
pytest tests/ -v --tb=short
```

All tests should pass. The hook system is now active with `PassthroughHook` as the zero-overhead default. To enable policy enforcement, add a `hooks:` section to `config.yaml`.
