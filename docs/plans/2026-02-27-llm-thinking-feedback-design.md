# Design: LLM Thinking Feedback in Web UI (Issue #42)

**Date:** 2026-02-27
**Issue:** https://github.com/timeplus-io/PulseBot/issues/42
**Branch:** feature/42-feedback-when-llm-is-thinking

## Problem

The web UI gives no visibility into LLM processing time. A user who sends a message sees
bouncing dots until the first tool call appears, then nothing again while the LLM processes
tool results. Users cannot see how long each LLM call takes or understand the full
reasoning sequence.

## Goal

Show the full agent execution trace in the web UI:

```
[LLM thinking... 3.2s]
[tool_call: web_search "timeplus streams"] (1.1s)
[LLM thinking... 1.8s]
[tool_call: run_query "SELECT ..."] (0.5s)
[LLM thinking... 2.1s]
Final response text
```

## Approach

Broadcast a new `llm_thinking` message type through the Timeplus messages stream before
and after each `llm.chat()` call, identical in pattern to the existing `tool_call`
broadcast. The server forwards these events over WebSocket. The UI renders them as
a thinking indicator row with live elapsed timer and final duration.

## Changes

### 1. `pulsebot/core/agent.py`

Add `_broadcast_llm_thinking()` method:

```python
async def _broadcast_llm_thinking(
    self,
    session_id: str,
    source: str,
    iteration: int,
    status: str,              # "started" | "completed"
    duration_ms: int = 0,
) -> None:
    content = {"status": status, "iteration": iteration}
    if duration_ms:
        content["duration_ms"] = duration_ms
    await self.messages_writer.write({
        "source": "agent",
        "target": f"channel:{source}",
        "session_id": session_id,
        "message_type": "llm_thinking",
        "content": json.dumps(content),
        "priority": 0,
    })
```

In `_process_message()`, wrap the `llm.chat()` call:

```python
await self._broadcast_llm_thinking(session_id, source, iteration, "started")
start_time = time.time()
response = await self.llm.chat(...)
latency_ms = (time.time() - start_time) * 1000
await self._broadcast_llm_thinking(session_id, source, iteration, "completed", int(latency_ms))
```

### 2. `pulsebot/api/server.py`

Add `'llm_thinking'` to the WebSocket query filter:

```python
AND message_type IN ('agent_response', 'tool_call', 'llm_thinking')
```

Forward to client:

```python
elif message_type == "llm_thinking":
    await websocket.send_json({
        "type": "llm_thinking",
        "status": content.get("status", ""),
        "iteration": content.get("iteration", 1),
        "duration_ms": content.get("duration_ms", 0),
    })
```

### 3. `pulsebot/web/index.html`

**CSS:** Reuse `.tool-call` classes. Add `llm-thinking` class for the thinking rows.
Use a sparkles/brain SVG instead of the gear icon.

**JavaScript:**

```javascript
const activeLlmThinking = new Map(); // iteration → {el, timerInterval}

function handleLlmThinking(data) {
    const key = data.iteration;
    if (data.status === 'started') {
        // Create indicator row with live elapsed timer
        const el = document.createElement('div');
        el.className = 'tool-call started llm-thinking';
        // ... render with shimmer, spinner, "Thinking..." label
        // Start setInterval to update elapsed seconds
        const startMs = Date.now();
        const timerEl = el.querySelector('.tool-call-status');
        const interval = setInterval(() => {
            timerEl.textContent = ((Date.now() - startMs) / 1000).toFixed(1) + 's...';
        }, 100);
        activeLlmThinking.set(key, { el, interval });
        messagesEl.appendChild(el);
        scrollToBottom();
    } else {
        // Update to completed state, stop timer
        const entry = activeLlmThinking.get(key);
        if (entry) {
            clearInterval(entry.interval);
            const durationS = (data.duration_ms / 1000).toFixed(1);
            // Update element to completed style with duration
            activeLlmThinking.delete(key);
        }
    }
}
```

Handle `llm_thinking` in `socket.onmessage`:

```javascript
} else if (data.type === 'llm_thinking') {
    hideTyping();
    handleLlmThinking(data);
}
```

## Event Lifecycle

| Time | Event | UI state |
|------|-------|----------|
| t=0 | User sends message | Typing indicator visible |
| t=0 | `llm_thinking {started, iter=1}` | Row: "Thinking... 0.0s" (counting) |
| t=3 | `llm_thinking {completed, iter=1, 3200ms}` | Row: "Thinking 3.2s" |
| t=3 | `tool_call {started}` | Tool row: "running..." |
| t=4 | `tool_call {success, 1100ms}` | Tool row: "1100ms" |
| t=4 | `llm_thinking {started, iter=2}` | New row: "Thinking... 0.0s" |
| t=6 | `llm_thinking {completed, iter=2, 1800ms}` | Row: "Thinking 1.8s" |
| t=6 | `agent_response` | Final message bubble |

## Non-goals

- No changes to stream DDL (message_type is a free-form string column)
- No streaming/token-by-token response — this is out of scope for this issue
- No Telegram channel support for thinking indicators (they go only to webchat)

## Testing

- Manual: Run agent with a query that triggers 2+ tool calls, verify full trace visible
- Verify timer counts up while LLM is processing
- Verify duration is accurate (close to actual LLM latency)
