# Scheduled Multi-Agent Projects — Design Spec

**Date:** 2026-03-24
**Status:** Approved
**Feature branch:** feature/scheduled-multi-agent-projects

---

## Problem

Multi-agent projects today are one-shot: the user (or LLM) calls `create_project`, agents run to completion, and all asyncio tasks exit. There is no way to run the same project topology on a recurring schedule — for example, a daily market research pipeline or an hourly system health report.

PulseBot already supports scheduled tasks for the main agent (interval and cron-based Timeplus Tasks that POST to `/api/v1/task-trigger`). This feature extends the same scheduling mechanism to multi-agent projects, with long-running agents that persist between runs and resume automatically after server restarts.

---

## Goals

- Run a multi-agent project on an interval or cron schedule.
- Agents remain alive between runs in an idle/waiting state (no re-spawn overhead).
- If a trigger fires while a run is in progress, skip it gracefully.
- On server restart, scheduled projects automatically recover and resume from their last checkpoint.
- Reuse the existing Timeplus Task scheduling infrastructure with minimal new abstractions.

---

## Non-Goals

- Dynamic modification of agent topology between runs (change agents by recreating the project).
- Fan-out of concurrent runs (at most one active run per project at any time).
- Per-run override of agent count or topology.

---

## Design

### 1. Data Model

No new streams are introduced. Four columns are added to `kanban_projects`.

#### `kanban_projects` — new columns

| Column | Type | Default | Description |
|---|---|---|---|
| `is_scheduled` | `bool` | `false` | True for scheduled projects |
| `schedule_type` | `string` | `''` | `'interval'` or `'cron'` |
| `schedule_expr` | `string` | `''` | e.g. `'30m'` or `'0 9 * * 1-5'` |
| `trigger_prompt` | `string` | `''` | Default instruction sent to the manager on each trigger |

**Append-only write invariant:** `kanban_projects` is append-only. Queries use `ORDER BY timestamp DESC LIMIT 1 BY project_id` to find the latest row per project. Any status-update row that omits the scheduling columns will cause those columns to appear empty, breaking recovery. Therefore **every insert into `kanban_projects` for a scheduled project — including status updates — must carry all four scheduling columns with their original values**. `ProjectManager` reads these from `ProjectState` (in-memory) when writing status rows.

#### `kanban_agents` — no changes

Already stores `checkpoint_sn uint64` — sufficient for both workers and the manager.

#### `pulsebot/agents/models.py` — updated models

**`SubAgentSpec`** — one new field:
```python
is_scheduled: bool = False
```

**`ProjectState`** — four new fields (carried in memory so live code never needs to re-query the stream):
```python
is_scheduled: bool = False
schedule_type: str = ""
schedule_expr: str = ""
trigger_prompt: str = ""
```

`pulsebot.tasks` (existing metadata stream) receives one record per scheduled project so it appears in the Tasks UI alongside regular scheduled tasks.

---

### 2. Trigger Flow

```
Timeplus Task (interval or cron)
  │  SQL fires on schedule, calls Python UDF:
  │  trigger_pulsebot_project(project_id, project_name, prompt)
  ▼
Python UDF
  │  POST /api/v1/projects/{project_id}/trigger
  │  Body: { "trigger_prompt": "..." }
  ▼
API Server  (POST /api/v1/projects/{project_id}/trigger)
  │  project not found → 404
  │  project busy      → 409 Skipped
  │  else              → _busy_projects.add(project_id)  [atomic w.r.t. asyncio]
  │                    → write to pulsebot.kanban:
  │      { msg_type: "trigger", target_id: "manager_{project_id}",
  │        project_id: ..., content: { prompt, project_id } }
  │                    → 200 { execution_id, session_id }
  ▼
ManagerAgent  (always running, idle)
  │  receives "trigger" msg from kanban stream
  │  dispatches task messages to workers (same as today)
  ▼
SubAgents / Workers  (always running, idle)
  │  receive "task" messages, execute LLM loop
  │  write results back to kanban targeting manager
  ▼
ManagerAgent
  │  collects worker results, synthesizes, delivers to session
  │  calls on_run_complete callback → ProjectManager.mark_project_idle(project_id)
  └─► back to idle, waiting for next trigger
```

#### New UDF: `trigger_pulsebot_project`

Parallel to the existing `trigger_pulsebot_task` UDF. Two new template strings are added to `tasks.py`: `_PROJECT_INTERVAL_UDF_TEMPLATE` and `_PROJECT_CRON_UDF_TEMPLATE`.

The `api_url` is an **embedding-time constant** — it is baked into the UDF body via `.format(api_url=api_url)` at task-creation time, not passed as a runtime argument. The UDF call signature has three runtime arguments (`project_id`, `project_name`, `prompt`):

```sql
CREATE TASK IF NOT EXISTS user_market_research
SCHEDULE 30m
TIMEOUT 30s
INTO pulsebot.task_triggers
AS SELECT
    trigger_pulsebot_project(
        'proj_9c766d2100e7',                                    -- project_id (embedded)
        'market research',                                       -- project_name (embedded)
        'Analyse the latest market trends and produce a report'  -- trigger_prompt (embedded)
    ) AS execution_id,
    now64(3) AS triggered_at
```

The UDF body POSTs to `{api_url}/api/v1/projects/{project_id}/trigger` (URL baked in at creation time).

#### New API endpoint

```
POST /api/v1/projects/{project_id}/trigger
Body: { "trigger_prompt": "..." }   # optional
```

If `trigger_prompt` is absent, `ProjectManager.trigger_project()` falls back to the value stored in `ProjectState.trigger_prompt` (in-memory), avoiding a stream round-trip on every trigger.

| Response | Meaning |
|---|---|
| `200` | Trigger accepted, run started |
| `409` | Project busy, trigger skipped |
| `404` | Project not found |

---

### 3. Agent Lifecycle

#### ManagerAgent changes

One new constructor parameter:

```python
on_run_complete: Callable[[], None] | None = None
# Called with no arguments after each run completes (scheduled projects only).
# ProjectManager passes a closure that calls mark_project_idle(project_id).
```

`ProjectManager.create_scheduled_project()` passes `lambda: self.mark_project_idle(project_id)` when constructing the manager.

| Behaviour | One-shot (today) | Scheduled (new) |
|---|---|---|
| After final result delivered | Exits loop | Calls `on_run_complete()`, continues loop |
| Cancel sent to workers | Yes | No |
| Handles `msg_type="trigger"` | No | Yes — starts a new run |

The `is_scheduled` flag on the manager's `SubAgentSpec` controls this branching. The one-shot code path is unchanged.

#### Manager checkpoint across runs

In scheduled mode the manager persists its `_checkpoint_sn` to `kanban_agents` after each kanban message processed (the same pattern workers already use). On boot recovery the manager is seeded with this checkpoint and uses `AND _tp_sn > {checkpoint_sn}` rather than a wall-clock `seek_to`. This ensures no trigger messages are missed or double-processed across restarts.

#### SubAgent (worker) changes

Workers are already long-running — they sit inside an infinite streaming query on `pulsebot.kanban`. The only change: for scheduled projects the manager **does not send `control: cancel`** at run completion. Workers return to idle automatically after processing their tasks.

#### Boot Recovery

`ProjectManager._recover_scheduled_projects()` is called from the **agent process** (`pulsebot run`) during startup, before the main agent loop begins.

Steps:
1. Query `kanban_projects` for `is_scheduled = true` AND `status = 'active'`, using `LIMIT 1 BY project_id` (returns the latest row, which carries scheduling fields due to the append-only write invariant in §1)
2. For each project, query `kanban_agents` for the latest `checkpoint_sn` per `agent_id`
3. Re-spawn `ManagerAgent` + workers with their recovered checkpoint values; agents resume from `_tp_sn > checkpoint_sn`
4. Call `CREATE TASK IF NOT EXISTS` for the associated Timeplus Task (idempotent)
5. Duplicate spawn guard: skip re-spawn if `agent_id` already has a running asyncio task

---

### 4. New Tool: `create_scheduled_project`

Added to `ProjectManagerSkill` alongside `create_project`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Human-readable project name |
| `description` | string | yes | What this project accomplishes |
| `agents` | array | yes | Worker agent specs (same schema as `create_project`) |
| `session_id` | string | yes | Session for routing final output |
| `schedule_type` | string | yes | `"interval"` or `"cron"` |
| `schedule_expr` | string | yes | e.g. `"30m"`, `"1h"`, `"0 9 * * 1-5"` |
| `trigger_prompt` | string | yes | Instruction sent to the manager on each scheduled run |
| `initial_messages` | array | no | Messages dispatched on first run only |

`ProjectManager.create_scheduled_project()`:

1. Validate `schedule_type` (`"interval"` or `"cron"`) and `schedule_expr` (non-empty)
2. Call existing `create_project()` logic; write all four scheduling columns into `kanban_projects`
3. Populate `ProjectState` with scheduling fields
4. Create the Timeplus Task via `TaskManager.create_project_interval_task()` or `create_project_cron_task()`
5. Write a record to `pulsebot.tasks` for Tasks UI visibility

#### New `TaskManager` methods

```python
def create_project_interval_task(
    self, project_id: str, project_name: str,
    trigger_prompt: str, interval: str, api_url: str,
) -> str: ...

def create_project_cron_task(
    self, project_id: str, project_name: str,
    trigger_prompt: str, cron: str, api_url: str,
) -> str: ...
```

Each method:
1. Creates (or replaces) the `trigger_pulsebot_project` Python UDF with `api_url` baked into the function body
2. Creates the Timeplus TASK with the schedule and embedded UDF call
3. Returns the sanitised task name (`user_{sanitised_project_name}`)

---

### 5. Busy State Tracking

`ProjectManager` maintains:

```python
_busy_projects: set[str]   # project_ids currently mid-run
```

**Concurrency safety:** PulseBot uses asyncio (single-threaded cooperative multitasking). The check-then-add in `trigger_project()` contains no `await` between the set check and the `add`, so it is atomic from asyncio's perspective. No locking primitive is required.

**Lifecycle:**

| Event | Action |
|---|---|
| `POST /projects/{id}/trigger` accepted | `_busy_projects.add(project_id)` before returning 200 |
| `ManagerAgent` run completes | `on_run_complete` → `mark_project_idle()` → `_busy_projects.discard(project_id)` |
| `delete_project()` called | `_busy_projects.discard(project_id)` |
| Server restart | `_busy_projects` starts empty (in-progress runs replay from checkpoint) |

---

### 6. Project Deletion

`delete_project` is extended:

1. Existing: cancel asyncio tasks, delete from kanban streams
2. New: `_busy_projects.discard(project_id)`
3. New: `DROP TASK IF EXISTS user_{sanitised_name}` — task name derived from `ProjectState.name` if in-memory, otherwise from the latest `kanban_projects` row

---

### 7. Pause / Resume

No new API needed. Reuse existing `TaskManager.pause_task()` / `resume_task()`. Pausing stops the Timeplus Task from firing; agents remain alive and idle. Resuming re-enables triggers at the next scheduled interval.

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Trigger fires while busy | `_busy_projects` check → 409; UDF discards; next fire handles it |
| Worker crashes mid-run | Manager times out (per `default_agent_timeout`), delivers partial result, calls `on_run_complete`, returns to idle |
| Server restart mid-run | Agents recover from `checkpoint_sn`; replay unprocessed kanban messages; complete run then go idle |
| Invalid schedule expression | Rejected at `create_scheduled_project` call time; error returned to LLM tool result |
| Scheduled project deleted while running | `delete_project` cancels tasks, discards from `_busy_projects`, drops Timeplus Task |
| Duplicate boot recovery spawn | Skip re-spawn if asyncio task for `agent_id` is not done |
| Status-update row drops scheduling fields | Prevented: all `kanban_projects` inserts read scheduling fields from `ProjectState` |

---

## Files Changed

| File | Change |
|---|---|
| `pulsebot/timeplus/setup.py` | Add `is_scheduled`, `schedule_type`, `schedule_expr`, `trigger_prompt` to `kanban_projects` DDL |
| `pulsebot/timeplus/tasks.py` | Add `_PROJECT_INTERVAL_UDF_TEMPLATE` and `_PROJECT_CRON_UDF_TEMPLATE` template strings; add `create_project_interval_task()` and `create_project_cron_task()` methods |
| `pulsebot/agents/models.py` | Add `is_scheduled` to `SubAgentSpec`; add `is_scheduled`, `schedule_type`, `schedule_expr`, `trigger_prompt` to `ProjectState` |
| `pulsebot/agents/manager_agent.py` | Add `on_run_complete` callback param; handle `trigger` msg_type; skip cancel-to-workers and call callback on run completion when scheduled; persist `checkpoint_sn` to `kanban_agents` in scheduled mode using `_tp_sn`-based seek |
| `pulsebot/agents/project_manager.py` | Add `_busy_projects: set`; add `create_scheduled_project()`, `trigger_project()`, `mark_project_idle()`, `_recover_scheduled_projects()`; extend `delete_project()` to discard from `_busy_projects` and drop Timeplus Task; ensure all `kanban_projects` status-update writes include scheduling fields from `ProjectState` |
| `pulsebot/skills/builtin/project_manager.py` | Add `create_scheduled_project` tool definition and handler |
| `pulsebot/api/server.py` | Add `POST /api/v1/projects/{project_id}/trigger` endpoint |
