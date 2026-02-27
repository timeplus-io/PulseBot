# LLM Thinking Feedback Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Show LLM thinking time and the full agent execution trace (LLM thinking → tool call → LLM thinking → ...) in the web UI.

**Architecture:** Broadcast a new `llm_thinking` message type through the Timeplus messages stream before and after each `llm.chat()` call, identical in pattern to the existing `tool_call` broadcast. The API server forwards these events over WebSocket. The web UI renders them as a thinking indicator row with live elapsed timer and final duration, matching the existing tool call UI pattern.

**Tech Stack:** Python asyncio (agent), FastAPI WebSocket (server), vanilla JS + CSS (frontend). No new dependencies.

---

### Task 1: Add `_broadcast_llm_thinking()` to agent and wire it around LLM calls

**Files:**
- Modify: `pulsebot/core/agent.py`

**Step 1: Add the `_broadcast_llm_thinking` method**

In `pulsebot/core/agent.py`, add this method after `_broadcast_tool_call` (around line 495):

```python
async def _broadcast_llm_thinking(
    self,
    session_id: str,
    source: str,
    iteration: int,
    status: str,
    duration_ms: int = 0,
) -> None:
    """Broadcast LLM thinking event to UI/CLI via messages stream.

    Args:
        session_id: Session identifier
        source: Original message source (for routing response)
        iteration: Agent loop iteration number (1-based)
        status: 'started' or 'completed'
        duration_ms: LLM call duration in milliseconds (for completed events)
    """
    content: dict[str, Any] = {"status": status, "iteration": iteration}
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

    logger.debug(
        f"LLM thinking broadcast: iteration={iteration} ({status})",
        extra={"session_id": session_id, "iteration": iteration},
    )
```

**Step 2: Wire the broadcasts around `llm.chat()` in `_process_message`**

In `_process_message`, find the agent loop (around line 224). Replace:

```python
# Call LLM
import time
start_time = time.time()

response = await self.llm.chat(
    messages=context.messages,
    tools=tools if tools else None,
    system=context.system_prompt,
)

latency_ms = (time.time() - start_time) * 1000
```

With:

```python
# Call LLM
import time
source = message.get("source", "webchat")
await self._broadcast_llm_thinking(session_id, source, iteration, "started")
start_time = time.time()

response = await self.llm.chat(
    messages=context.messages,
    tools=tools if tools else None,
    system=context.system_prompt,
)

latency_ms = (time.time() - start_time) * 1000
await self._broadcast_llm_thinking(session_id, source, iteration, "completed", int(latency_ms))
```

Note: `source` is already extracted from `message` earlier via `message.get("source", "webchat")` — check the existing code. In `_broadcast_tool_call` calls (lines ~259, ~284) you'll see `source=message.get("source", "webchat")`. You can assign `source` once at the top of the while loop using `message.get("source", "webchat")` and reuse it, or just inline it in each call.

**Step 3: Verify no test regressions**

Run: `pytest -v 2>&1 | tail -20`
Expected: All existing tests pass (there are no agent loop tests that mock stream writes at this level, so this should be clean).

**Step 4: Commit**

```bash
git add pulsebot/core/agent.py
git commit -m "feat: broadcast llm_thinking events around each LLM call

Emits started/completed events before and after each llm.chat() call
in the agent loop, carrying iteration number and duration_ms. Pattern
mirrors existing tool_call broadcasts.

Closes #42"
```

---

### Task 2: Forward `llm_thinking` events through the WebSocket server

**Files:**
- Modify: `pulsebot/api/server.py`

**Step 1: Add `llm_thinking` to the stream query filter**

In `server.py`, in the `send_responses()` function (around line 237), find:

```python
AND message_type IN ('agent_response', 'tool_call')
```

Replace with:

```python
AND message_type IN ('agent_response', 'tool_call', 'llm_thinking')
```

**Step 2: Add the `llm_thinking` forwarding branch**

In the `send_responses()` message handling block (around lines 263-284), find:

```python
if message_type == "tool_call":
    # Send tool call event
    await websocket.send_json({
        ...
    })
    logger.debug(...)
else:
    # Send regular response
    ...
```

Change to a three-way branch:

```python
if message_type == "tool_call":
    # Send tool call event
    await websocket.send_json({
        "type": "tool_call",
        "tool_name": content.get("tool_name", ""),
        "status": content.get("status", ""),
        "arguments": content.get("arguments", {}),
        "args_summary": content.get("args_summary", ""),
        "result_preview": content.get("result_preview", ""),
        "duration_ms": content.get("duration_ms", 0),
        "message_id": message.get("id", ""),
    })
    logger.debug(f"Sent tool_call to WebSocket: {content.get('tool_name')}")
elif message_type == "llm_thinking":
    # Send LLM thinking event
    await websocket.send_json({
        "type": "llm_thinking",
        "status": content.get("status", ""),
        "iteration": content.get("iteration", 1),
        "duration_ms": content.get("duration_ms", 0),
        "message_id": message.get("id", ""),
    })
    logger.debug(f"Sent llm_thinking to WebSocket: iteration={content.get('iteration')} status={content.get('status')}")
else:
    # Send regular response
    text = content.get("text", "")
    logger.info(f"Sending response to WebSocket: {session_id}, text length: {len(text)}")
    await websocket.send_json({
        "type": "response",
        "text": text,
        "message_id": message.get("id", ""),
    })
```

**Step 3: Commit**

```bash
git add pulsebot/api/server.py
git commit -m "feat: forward llm_thinking events through WebSocket

Adds llm_thinking to the stream query filter and forwards events
to WebSocket clients with type, status, iteration, and duration_ms."
```

---

### Task 3: Render LLM thinking indicators in the web UI

**Files:**
- Modify: `pulsebot/web/index.html`

This is the largest change. It has three parts: CSS, state variables, and the `handleLlmThinking` function.

**Step 1: Add CSS for the LLM thinking indicator**

After the `.tool-call.error .tool-call-details` rule (around line 440), add:

```css
/* LLM Thinking Indicator */
.llm-thinking .tool-call-name {
    color: var(--gray-600);
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 13px;
}

.llm-thinking.completed .tool-call-name {
    color: var(--gray-500);
}

.llm-thinking.completed {
    background: var(--gray-50);
    border-color: var(--gray-200);
    opacity: 0.75;
}
```

**Step 2: Add state variable for active LLM thinking calls**

After the `const activeToolCalls = new Map();` line (around line 783), add:

```javascript
// Track active LLM thinking calls by iteration (for updating when completed)
const activeLlmThinking = new Map(); // iteration → {el, timerInterval, startMs}
```

**Step 3: Add `handleLlmThinking` function**

After the `handleToolCall` function (after line 838), add:

```javascript
// Handle LLM thinking events
function handleLlmThinking(data) {
    // Hide empty state
    emptyStateEl.style.display = 'none';

    const iteration = data.iteration || 1;

    if (data.status === 'started') {
        const startMs = Date.now();

        const thinkingEl = document.createElement('div');
        thinkingEl.className = 'tool-call started llm-thinking';
        thinkingEl.innerHTML = `
            <div class="tool-call-header">
                <svg class="tool-call-icon spinning" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.346.346a.5.5 0 01-.16.113l-.342.15a.5.5 0 01-.195.04H9.5a.5.5 0 01-.195-.04l-.342-.15a.5.5 0 01-.16-.113l-.346-.346z"/>
                </svg>
                <div style="display: flex; flex-direction: column; flex: 1;">
                    <span class="tool-call-name">Thinking</span>
                </div>
                <span class="tool-call-status" id="llm-thinking-timer-${iteration}">0.0s...</span>
            </div>
        `;

        messagesEl.appendChild(thinkingEl);
        scrollToBottom();

        // Update timer every 100ms
        const timerEl = thinkingEl.querySelector(`#llm-thinking-timer-${iteration}`);
        const interval = setInterval(() => {
            const elapsed = ((Date.now() - startMs) / 1000).toFixed(1);
            timerEl.textContent = `${elapsed}s...`;
        }, 100);

        activeLlmThinking.set(iteration, { el: thinkingEl, interval, startMs });

    } else {
        // Completed - stop timer, show final duration
        const entry = activeLlmThinking.get(iteration);
        if (entry) {
            clearInterval(entry.interval);
            const durationS = (data.duration_ms / 1000).toFixed(1);

            entry.el.className = 'tool-call llm-thinking completed';
            entry.el.innerHTML = `
                <div class="tool-call-header">
                    <svg class="tool-call-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.346.346a.5.5 0 01-.16.113l-.342.15a.5.5 0 01-.195.04H9.5a.5.5 0 01-.195-.04l-.342-.15a.5.5 0 01-.16-.113l-.346-.346z"/>
                    </svg>
                    <div style="display: flex; flex-direction: column; flex: 1;">
                        <span class="tool-call-name">Thinking</span>
                    </div>
                    <span class="tool-call-status">${durationS}s</span>
                </div>
            `;
            activeLlmThinking.delete(iteration);
        }
    }
}
```

**Step 4: Wire `handleLlmThinking` into the WebSocket message handler**

Find `socket.onmessage` (around line 722):

```javascript
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'response') {
        hideTyping();
        removeToolCallIndicators();
        addMessage(data.text, 'assistant');
        isWaitingForResponse = false;
        updateSendButton();
    } else if (data.type === 'tool_call') {
        hideTyping();
        handleToolCall(data);
    }
};
```

Replace with:

```javascript
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'response') {
        hideTyping();
        removeToolCallIndicators();
        addMessage(data.text, 'assistant');
        isWaitingForResponse = false;
        updateSendButton();
    } else if (data.type === 'tool_call') {
        hideTyping();
        handleToolCall(data);
    } else if (data.type === 'llm_thinking') {
        hideTyping();
        handleLlmThinking(data);
    }
};
```

**Step 5: Verify the full flow manually**

Start the server and agent (`pulsebot serve` + `pulsebot run`), open the web UI, send a message that triggers a tool call, and verify:
- "Thinking" row appears with counting timer immediately after message is sent
- Timer counts up while LLM processes
- When "completed" arrives, timer stops and shows e.g. "3.2s"
- Tool call indicator appears next
- Another "Thinking" row appears for the next LLM call
- Final response renders normally

**Step 6: Commit**

```bash
git add pulsebot/web/index.html
git commit -m "feat: render LLM thinking indicators in web UI

Adds handleLlmThinking() function that shows a thinking row with
live elapsed timer while the LLM is processing, then updates to
show final duration when complete. Matches the visual style of
existing tool call indicators."
```

---

### Task 4: Clean up timer state on disconnect/reconnect

**Files:**
- Modify: `pulsebot/web/index.html`

When the WebSocket disconnects or a new session starts, any in-progress timer intervals must be cleared to avoid memory leaks.

**Step 1: Add cleanup to `connect()` reconnect logic**

Find the `socket.onclose` handler (around line 736):

```javascript
socket.onclose = () => {
    isConnected = false;
    updateStatus(false);
    console.log('Disconnected from PulseBot');
    // Attempt to reconnect after 3 seconds
    setTimeout(connect, 3000);
};
```

Replace with:

```javascript
socket.onclose = () => {
    isConnected = false;
    updateStatus(false);
    console.log('Disconnected from PulseBot');
    // Clear any in-progress thinking timers
    activeLlmThinking.forEach(entry => clearInterval(entry.interval));
    activeLlmThinking.clear();
    // Attempt to reconnect after 3 seconds
    setTimeout(connect, 3000);
};
```

**Step 2: Commit**

```bash
git add pulsebot/web/index.html
git commit -m "fix: clear LLM thinking timers on WebSocket disconnect

Prevents timer interval leaks when the connection drops and a
new session is started."
```

---

### Task 5: Final verification and PR

**Step 1: Run all tests**

```bash
pytest -v
```

Expected: All pass.

**Step 2: Create pull request**

```bash
gh pr create \
  --title "feat: show LLM thinking time in web UI (issue #42)" \
  --body "Closes #42

## What

Shows LLM thinking indicators in the web UI so users can see the full agent execution trace:

\`\`\`
[Thinking 3.2s]
[tool_call: web_search] (1.1s)
[Thinking 1.8s]
Final response
\`\`\`

## How

- Agent broadcasts \`llm_thinking\` stream events before/after each \`llm.chat()\` call
- Server forwards these over WebSocket alongside existing \`tool_call\` events
- UI renders a thinking row with live elapsed timer while in progress, then shows final duration when complete
- Visual style matches existing tool call indicators" \
  --base main
```
