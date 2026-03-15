# Tool Call Hooks

PulseBot's hook system lets you intercept every tool call the agent makes — before execution (to approve, deny, or modify it) and after execution (for observability).

## Overview

Hooks are configured under `hooks.tool_call` in `config.yaml`. The design is forward-compatible: `tool_call` is one namespace under `hooks`, leaving room for `llm_call` and other hook types in the future.

```
Agent
 └─ ToolExecutor.execute(tool_name, arguments)
      ├─ [pre_call hooks] → approve / deny / modify
      ├─ skill.execute(tool_name, effective_arguments)
      └─ [post_call hooks] → observe result
```

**Pre-call hooks** run in sequence before the skill executes:
- Any hook can return `deny` → execution stops immediately, remaining hooks are skipped.
- Any hook can return `modify` → subsequent hooks and the skill receive the modified arguments.
- `approve` continues to the next hook.

**Post-call hooks** run after execution regardless of pre-call results. Errors in post-call hooks are logged but never propagate to the caller.

## Default Behavior

When no `hooks:` section is present in `config.yaml`, a `PassthroughHook` is used automatically. It approves every call with zero overhead.

## Configuration

```yaml
hooks:
  tool_call:
    pre_call:
      - type: <hook-type>
        config:
          <hook-specific-options>
```

## Built-in Hook Types

### `passthrough`

Approves everything. Useful as an explicit placeholder or to reset a chain.

```yaml
hooks:
  tool_call:
    pre_call:
      - type: passthrough
```

No `config` options.

---

### `policy`

Evaluates tool calls against allow/deny lists and argument content rules.

**Evaluation order** (first match wins):
1. `deny_tools` — if tool name matches, deny immediately.
2. `deny_argument_patterns` — if any argument value matches a regex, deny.
3. `allow_tools` — if set and tool name does not match, deny.
4. Otherwise → approve.

| Config field | Type | Description |
| :--- | :--- | :--- |
| `allow_tools` | `list[str]` | Whitelist of tool name patterns (fnmatch wildcards supported). |
| `deny_tools` | `list[str]` | Blacklist of tool name patterns. Takes absolute precedence. |
| `deny_argument_patterns` | `dict[str, list[str]]` | Map of argument key → regex patterns. Blocks matching values. |

**Examples:**

```yaml
# Allow only file tools
- type: policy
  config:
    allow_tools: ["read_file", "write_file", "list_directory"]

# Block dangerous shell patterns
- type: policy
  config:
    deny_argument_patterns:
      command: ["rm -rf", "sudo", "curl.*\\|.*sh"]

# Wildcards: allow any file_* tool, block everything else
- type: policy
  config:
    allow_tools: ["file_*"]
```

---

### `webhook`

POSTs tool call information to an external HTTP endpoint and uses the response to decide whether to allow the call.

**Request body (POST):**
```json
{
  "tool_name": "run_command",
  "arguments": {"command": "ls -la"},
  "session_id": "abc123"
}
```

**Expected response body:**
```json
{
  "verdict": "approve",          // "approve", "deny", or "modify"
  "reasoning": "optional note",
  "modified_arguments": {}       // only for verdict "modify"
}
```

| Config field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `url` | `str` | _(required)_ | HTTP/HTTPS endpoint to POST to. |
| `auth_header` | `str` | `""` | `Authorization` header value (e.g., `Bearer <token>`). |
| `timeout` | `float` | `5.0` | Request timeout in seconds. |
| `fail_open` | `bool` | `true` | If `true`, approve on network/timeout errors. If `false`, deny. |

**Example:**

```yaml
- type: webhook
  config:
    url: "https://your-approval-service.example.com/hook"
    auth_header: "Bearer ${WEBHOOK_SECRET}"
    timeout: 5.0
    fail_open: true
```

The webhook also receives `post_call` notifications after execution (with an `"event": "post_call"` field added), useful for audit logging.

---

## Chaining Multiple Hooks

Hooks run in order. The first `deny` short-circuits the chain.

```yaml
hooks:
  tool_call:
    pre_call:
      # 1. Fast local policy check (no network)
      - type: policy
        config:
          deny_tools: ["run_command"]

      # 2. External audit/approval for everything else
      - type: webhook
        config:
          url: "https://audit.example.com/hook"
          fail_open: true
```

---

## Writing a Custom Hook

Subclass `ToolCallHook` from `pulsebot.hooks.base`:

```python
from pulsebot.hooks.base import HookVerdict, ToolCallHook

class MyHook(ToolCallHook):
    async def pre_call(self, tool_name, arguments, session_id="") -> HookVerdict:
        if tool_name == "run_command" and "sudo" in arguments.get("command", ""):
            return HookVerdict(verdict="deny", reasoning="sudo not allowed")
        return HookVerdict(verdict="approve")

    async def post_call(self, tool_name, arguments, result, session_id="") -> None:
        print(f"{tool_name} → success={result['success']}")
```

Pass it directly to `ToolExecutor`:

```python
from pulsebot.core.executor import ToolExecutor
executor = ToolExecutor(skill_loader, hooks=[MyHook()])
```

Or register it in the hook registry (so it can be used from `config.yaml`):

```python
from pulsebot.hooks.factory import _HOOK_REGISTRY
_HOOK_REGISTRY["my_hook"] = MyHook
```

---

## Verdict Reference

| Verdict | Effect |
| :--- | :--- |
| `approve` | Continue to the next hook (or execute the tool if last). |
| `deny` | Stop immediately. Tool is not executed. Agent receives an error result. |
| `modify` | Replace `arguments` with `modified_arguments` for all subsequent hooks and the tool itself. |

---

## Roadmap

- **`HumanApprovalHook`** — pause the agent and ask a human via the messages stream before proceeding.
- **`llm_call` hooks** — intercept LLM API calls (under `hooks.llm_call`).
