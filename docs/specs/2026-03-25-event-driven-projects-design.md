# Event-Driven Multi-Agent Projects — Design Spec

**Date:** 2026-03-25
**Status:** Approved
**Feature branch:** feature/event-driven-multi-agent-projects

---

## Problem

Multi-agent projects currently support two execution modes:

1. **One-shot** — runs once and exits.
2. **Scheduled** — runs on a fixed interval or cron schedule via a Timeplus Task UDF.

Neither mode supports reacting to real-time streaming data. There is no way to say "run this agent workflow every time an error event appears in the event stream" or "trigger this pipeline whenever a sensor reading exceeds a threshold." This feature adds a third mode: **event-driven**, where a Proton streaming SQL query is the trigger source and each result row fires one workflow run.

---

## Goals

- Trigger a multi-agent workflow once per matching row from a user-defined Proton streaming query.
- Skip incoming events while a run is in progress (no queuing; drop-on-busy).
- Extract a single designated column from each row and inject its value into the agents' trigger prompt.
- Survive server restarts: resume the streaming query from the last checkpointed sequence number so no events are missed or double-processed.
- Reuse the existing ManagerAgent scheduled-mode code path with minimal changes to that component.

---

## Non-Goals

- Per-batch or windowed aggregation triggering (may be added later).
- Template-based prompt construction with multiple column placeholders (may be added later; current design uses a single context field).
- Concurrent parallel runs within one project (at most one active run at any time).
- Modifying agent topology between runs.

---

## Design

### 1. Data Model

No new streams are introduced. Two new columns are added to `kanban_projects`, and `schedule_type` gains a third valid value: `'event'`.

#### `kanban_projects` — new columns

| Column | Type | Default | Description |
|---|---|---|---|
| `event_query` | `string` | `''` | Complete Proton streaming SQL to subscribe to |
| `context_field` | `string` | `''` | Column name in the query result to extract as trigger context |

These columns are empty for one-shot and scheduled projects.

#### `schedule_type` values

| Value | Meaning |
|---|---|
| `''` | One-shot project (`is_scheduled = false`) |
| `'interval'` | Fixed-interval scheduled project |
| `'cron'` | Cron-scheduled project |
| `'event'` | Event-driven project (new) |

#### Append-only write invariant

`kanban_projects` is append-only; queries use `ORDER BY timestamp DESC LIMIT 1 BY project_id` to get the latest state. Every insert for an event-driven project — including status-update rows — must carry all scheduling and event fields (`is_scheduled`, `schedule_type`, `event_query`, `context_field`, `trigger_prompt`) from `ProjectState`. This prevents recovery failures caused by empty scheduling fields in status rows.

#### `pulsebot/agents/models.py` — updated fields

**`SubAgentSpec`** — two new fields:
```python
event_query: str = ""
context_field: str = ""
```

**`ProjectState`** — two new fields:
```python
event_query: str = ""
context_field: str = ""
```

#### `kanban_agents` — one extra checkpoint row per event-driven project

`EventWatcher` persists its streaming query sequence number as a `kanban_agents` row with:
- `agent_id = f"event_watcher_{project_id}"`
- `checkpoint_sn` = last processed `_tp_sn`

Recovery reads this row on startup exactly as worker agents read theirs.

---

### 2. EventWatcher Component

A new focused class in `pulsebot/agents/event_watcher.py`.

**Responsibility:** Subscribe to the user's streaming query, extract the context field from each row, and call `trigger_project_with_context()` if the project is not busy. Checkpoint the streaming query's `_tp_sn` after every row processed (whether skipped or triggered).

#### Interface

```python
class EventWatcher:
    def __init__(
        self,
        project_id: str,
        event_query: str,
        context_field: str,
        trigger_prompt: str,
        project_manager: ProjectManager,
        timeplus: TimeplusClient,
        config: Config,
        checkpoint_sn: int = 0,
        start_time: datetime | None = None,
        # ProjectManager passes datetime.now(timezone.utc) at instantiation.
        # None is only valid in tests; production code always provides a value.
    ) -> None: ...

    async def run(self) -> None: ...         # main async loop
    def stop(self) -> None: ...              # set _running = False
```

#### Streaming query construction

The user provides a bare streaming SQL that queries **a single Proton stream or view directly** (not a nested subquery). This constraint is required because `_tp_sn` is a virtual column on the physical stream and its visibility through subquery boundaries in Proton is not guaranteed.

`EventWatcher` appends seek control and optional `_tp_sn` filtering to the user's query:

**First run (no checkpoint):**
```sql
{event_query} SETTINGS seek_to='{start_time}'
```

**After restart with checkpoint:**
```sql
{event_query} AND _tp_sn > {checkpoint_sn} SETTINGS seek_to='earliest'
```

`_tp_sn` is accessed as a system column from each row returned by the `StreamReader`, the same way `ManagerAgent._run_scheduled()` accesses it from the kanban query.

> **Constraint:** `event_query` must be a `SELECT ... FROM <stream_or_view> [WHERE ...]` query. Nested subqueries are not supported because `_tp_sn` may not propagate through subquery boundaries in Proton. This should be validated at `create_event_driven_project()` time (reject queries containing `FROM (`).

#### Per-row logic

```
outer loop (while _running):
    rebuild streaming query from current checkpoint
    for each row in streaming_query.stream(query):
        context_value = row.get(context_field, "")
        if context_value is empty:
            log warning, persist checkpoint, continue
        if project_manager.is_project_busy(project_id):
            log debug "event skipped — run in progress"
            persist checkpoint (_tp_sn)
            continue
        combined_prompt = f"{trigger_prompt}\n\n{context_value}"
        project_manager.trigger_project_with_context(project_id, combined_prompt)
        persist checkpoint (_tp_sn)
    if stream closed unexpectedly:
        log warning, reconnect after short delay
```

Skipped events advance the checkpoint — they are intentionally dropped, not queued for replay.

#### Reconnect behaviour

If the Proton streaming connection closes (the inner `async for` loop ends without `_running` being False), the outer `while _running` loop restarts the query from the last persisted checkpoint. This is identical to the pattern in `ManagerAgent._run_scheduled()`.

---

### 3. Trigger Flow

```
Proton streaming query (user-defined SQL)
  │
  ▼  row arrives
EventWatcher
  │  extract context_field value from row
  │  project busy? ──yes──► skip, advance checkpoint, continue
  │  not busy?
  │    mark busy (_busy_projects.add)
  │    write trigger kanban message:
  │      { msg_type: "trigger",
  │        target_id: "manager_{project_id}",
  │        project_id: ...,
  │        content: {"prompt": "{trigger_prompt}\n\n{context_value}"} }
  │    advance checkpoint
  ▼
ManagerAgent  (scheduled mode — zero changes required)
  │  receives "trigger" kanban message
  │  dispatches task messages to source workers with combined prompt
  ▼
Worker agents execute LLM loop
  │  return results to manager via kanban
  ▼
ManagerAgent
  │  collects results, broadcasts via task_notification event
  │  calls on_run_complete callback
  ▼
ProjectManager.mark_project_idle(project_id)
  │  _busy_projects.discard(project_id)
  ▼
EventWatcher is free to process the next event row
```

**ManagerAgent changes (minimal):** `_update_project_status()` must write `event_query` and `context_field` alongside the existing scheduling fields to satisfy the append-only write invariant. Since `ManagerAgent` already stores these on `self.spec` (populated by `ProjectManager` at construction), no new constructor parameters are needed — only the `_update_project_status()` insert is updated. All other ManagerAgent logic (trigger handling, worker dispatch, run completion) is unchanged.

No Timeplus Task UDF is needed for event-driven projects.

---

### 4. ProjectManager Changes

#### New method: `create_event_driven_project()`

1. Validate `event_query` (non-empty) and `context_field` (non-empty, valid identifier).
2. Call the existing internal project-creation logic (spawn ManagerAgent + workers, write `kanban_projects` row with all fields including `event_query`, `context_field`, `schedule_type='event'`, `is_scheduled=True`).
3. Instantiate and start `EventWatcher` as an asyncio task.
4. Store the EventWatcher task reference alongside manager/worker tasks for lifecycle management.

#### New internal method: `trigger_project_with_context(project_id, prompt)`

Writes the trigger kanban message and adds to `_busy_projects`. Called by `EventWatcher`. Not exposed via HTTP (the existing `/api/v1/projects/{project_id}/trigger` endpoint can still manually trigger event-driven projects for testing).

#### Extended: `_recover_scheduled_projects()`

The SELECT list in the recovery query is extended to include `event_query` and `context_field`:

```sql
SELECT project_id, name, description, session_id, schedule_type, schedule_expr,
       trigger_prompt, agent_ids, event_query, context_field
FROM table(pulsebot.kanban_projects)
WHERE is_scheduled = true AND status = 'active'
ORDER BY timestamp DESC LIMIT 1 BY project_id
```

On boot, for each active scheduled project:
- `schedule_type in ('interval', 'cron')` → existing path: create Timeplus Task + spawn manager + workers.
- `schedule_type == 'event'` → new path: spawn manager + workers + `EventWatcher` (with recovered checkpoint from `kanban_agents` row `event_watcher_{project_id}`). No Timeplus Task created.

#### Extended: `_write_project_metadata()`

Signature extended with two new optional parameters (defaulting to `""` so existing callers are unaffected):

```python
def _write_project_metadata(
    self, ...,
    event_query: str = "",
    context_field: str = "",
) -> None: ...
```

The insert includes both new columns for all project types (empty string for non-event projects).

#### Extended: `delete_project()`

- If the project has an associated `EventWatcher` asyncio task, cancel it before removing project state.
- The Timeplus Task drop call is guarded: `if state.schedule_type in ('interval', 'cron'): drop_task(...)`. Event-driven projects have no Timeplus Task and must not attempt to drop one.

---

### 5. New LLM Tool: `create_event_driven_project`

Added to `ProjectManagerSkill` alongside `create_project` and `create_scheduled_project`.

#### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Human-readable project name |
| `description` | string | yes | What this project accomplishes |
| `agents` | array | yes | Worker agent specs (same schema as existing tools) |
| `session_id` | string | yes | Session for routing output |
| `event_query` | string | yes | Streaming SQL to subscribe to (must SELECT the `context_field` column) |
| `context_field` | string | yes | Column name in query result to extract as trigger context |
| `trigger_prompt` | string | yes | Instruction prefix; combined with extracted context value as `"{trigger_prompt}\n\n{context_value}"` |
| `initial_messages` | array | no | Messages dispatched once on project creation |

#### Example

```
event_query:    "SELECT payload FROM pulsebot.events WHERE severity = 'error'"
context_field:  "payload"
trigger_prompt: "A system error was detected. Investigate and summarize:"
```

Combined prompt delivered to workers:
```
A system error was detected. Investigate and summarize:

{"source": "agent:xyz", "message": "Connection refused on port 8463"}
```

---

### 6. Error Handling

| Scenario | Behaviour |
|---|---|
| `context_field` not found in query result row | Log warning, skip row, advance checkpoint — do not crash |
| `context_field` value is empty string | Log warning, skip row, advance checkpoint |
| Streaming query returns no rows (stream empty or no matching events) | EventWatcher idles in the open streaming connection; reconnects if connection closes |
| Proton closes the streaming connection unexpectedly | Outer reconnect loop restarts query from last checkpoint after a short delay |
| Invalid SQL in `event_query` | Proton returns error on first `stream()` call; EventWatcher logs error and retries with backoff (3s, 10s, 30s cap) |
| Event arrives while project is busy | Skipped; checkpoint advanced; logged at debug level |
| Server restart while a run is mid-flight | Workers and manager recover from kanban checkpoint and complete the run; EventWatcher recovers from its own checkpoint and resumes listening |
| Server restart while EventWatcher is idle (between events) | EventWatcher resumes from checkpoint; no events missed (replayed from `_tp_sn`) |
| Project deleted while EventWatcher running | `delete_project()` cancels the asyncio task; EventWatcher stops cleanly |
| Duplicate recovery spawn on boot | Skip re-spawn if an asyncio task for `agent_id` already exists and is not done |

---

## Files Changed

| File | Change |
|---|---|
| `pulsebot/timeplus/setup.py` | Add `event_query string DEFAULT ''` and `context_field string DEFAULT ''` to `kanban_projects` DDL |
| `pulsebot/agents/models.py` | Add `event_query: str = ""`, `context_field: str = ""` to `SubAgentSpec` and `ProjectState` |
| `pulsebot/agents/event_watcher.py` | **New file** — `EventWatcher` class with streaming query subscription, per-row trigger logic, checkpoint persistence, and reconnect loop |
| `pulsebot/agents/manager_agent.py` | Update `_update_project_status()` to include `event_query` and `context_field` from `self.spec` in every `kanban_projects` insert |
| `pulsebot/agents/project_manager.py` | Add `create_event_driven_project()`, `trigger_project_with_context()`; extend `_recover_scheduled_projects()` SELECT list and dispatch path; extend `_write_project_metadata()` signature; extend `delete_project()` with EventWatcher cancellation and `schedule_type` guard on Timeplus Task drop |
| `pulsebot/skills/builtin/project_manager.py` | Add `create_event_driven_project` tool definition and `_create_event_driven_project()` handler |
