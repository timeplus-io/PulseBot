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

No new streams are introduced. Three columns are added to `kanban_projects` and one to the Timeplus Task metadata:

#### `kanban_projects` — new columns

| Column | Type | Default | Description |
|---|---|---|---|
| `is_scheduled` | `bool` | `false` | True for scheduled projects |
| `schedule_type` | `string` | `''` | `'interval'` or `'cron'` |
| `schedule_expr` | `string` | `''` | e.g. `'30m'` or `'0 9 * * 1-5'` |
| `trigger_prompt` | `string` | `''` | Default instruction sent to the manager on each trigger |

`kanban_agents` already stores `checkpoint_sn uint64` — no changes required.

`pulsebot.tasks` (existing metadata stream) receives one record per scheduled project so it appears in the Tasks UI alongside regular scheduled tasks.

#### `SubAgentSpec` — new field

```python
is_scheduled: bool = False   # propagated from project creation
```

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
API Server  (/api/v1/projects/{project_id}/trigger)
  │  project not found → 404
  │  project busy      → 409 Skipped (UDF logs, Timeplus discards)
  │  else              → write to pulsebot.kanban:
  │      { msg_type: "trigger", target_id: "manager_{project_id}",
  │        project_id: ..., content: { prompt, project_id } }
  │                    → 200 { execution_id, session_id }
  ▼
ManagerAgent  (always running, idle)
  │  receives "trigger" msg from kanban stream
  │  sets _busy = True
  │  dispatches task messages to workers (same as today)
  ▼
SubAgents / Workers  (always running, idle)
  │  receive "task" messages, execute LLM loop
  │  write results back to kanban targeting manager
  ▼
ManagerAgent
  │  collects worker results, synthesizes, delivers to session
  │  sets _busy = False
  └─► back to idle, waiting for next trigger
```

#### New UDF: `trigger_pulsebot_project`

Parallel to the existing `trigger_pulsebot_task` UDF. Embedded in the Timeplus Task at creation time with the `project_id` and base URL hardcoded:

```sql
CREATE TASK IF NOT EXISTS user_market_research
SCHEDULE 30m
TIMEOUT 30s
INTO pulsebot.task_triggers
AS SELECT
    trigger_pulsebot_project(
        'proj_9c766d2100e7',
        'market research',
        'Analyse the latest market trends and produce a summary report'
    ) AS execution_id,
    now64(3) AS triggered_at
```

#### New API endpoint

```
POST /api/v1/projects/{project_id}/trigger
Body: { "trigger_prompt": "..." }   # optional; overrides stored trigger_prompt for this run
```

| Response | Meaning |
|---|---|
| `200` | Trigger accepted, run started |
| `409` | Project busy, trigger skipped |
| `404` | Project not found |

### 3. Agent Lifecycle

#### ManagerAgent changes

| Behaviour | One-shot (today) | Scheduled (new) |
|---|---|---|
| After final result delivered | Exits loop | Sets `_busy=False`, continues loop |
| Cancel sent to workers | Yes | No |
| Handles `msg_type="trigger"` | No | Yes — starts a new run |
| `_busy` flag | Not present | Added; guards against concurrent runs |

The `is_scheduled` flag on the manager spec controls this branching. No changes to the one-shot code path.

#### SubAgent (worker) changes

Workers are already long-running — they sit inside an infinite streaming query on `pulsebot.kanban` and process messages as they arrive. The only change: for scheduled projects the manager **does not send `control: cancel`** at run completion. Workers automatically return to idle after processing their tasks.

#### Boot Recovery

`ProjectManager._recover_scheduled_projects()` is called during `startup()`:

1. Query `kanban_projects` for rows where `is_scheduled = true` AND `status = 'active'`
2. For each project, query `kanban_agents` for the latest `checkpoint_sn` per `agent_id`
3. Re-spawn `ManagerAgent` + workers with their recovered checkpoint values
4. Call `CREATE TASK IF NOT EXISTS` for the associated Timeplus Task (idempotent)

Agents resume the kanban stream from their checkpoint sequence number. Workers that were mid-task when the server stopped will replay unprocessed messages and complete the interrupted run before returning to idle.

Duplicate spawn guard: before creating an asyncio task for an `agent_id`, check whether one is already running (`not task.done()`).

### 4. New Tool: `create_scheduled_project`

Added to `ProjectManagerSkill` alongside `create_project`. Parameters:

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

`ProjectManager.create_scheduled_project()` implementation:

1. Validate `schedule_type` and `schedule_expr`
2. Call existing `create_project()` logic with `is_scheduled=True` added to `kanban_projects` write
3. Create the Timeplus Task via `TaskManager.create_project_interval_task()` or `create_project_cron_task()`
4. Write a record to `pulsebot.tasks` for Tasks UI visibility

#### New `TaskManager` methods

```python
def create_project_interval_task(
    self, project_id: str, project_name: str,
    trigger_prompt: str, interval: str, api_url: str
) -> str: ...

def create_project_cron_task(
    self, project_id: str, project_name: str,
    trigger_prompt: str, cron: str, api_url: str
) -> str: ...
```

Task name derived as: `user_{sanitised_project_name}` (same sanitisation as regular tasks).

### 5. Busy State Tracking

`ProjectManager` maintains:

```python
_busy_projects: set[str]   # project_ids currently mid-run
```

- Set on `trigger_project(project_id)` before writing the kanban trigger message
- Cleared when `ManagerAgent` completes a run (manager calls back via a new `ProjectManager.mark_project_idle(project_id)` method)
- The `/api/v1/projects/{project_id}/trigger` endpoint checks this set synchronously before writing to kanban — if busy, returns 409 immediately

`ProjectManager` is already injected into the API server as a singleton, so the in-memory set is shared. This does not survive restarts — on restart `_busy_projects` starts empty, which is correct (any in-progress run will be replayed from checkpoint).

### 6. Project Deletion

`delete_project` is extended:

1. Existing: cancel asyncio tasks, delete from kanban streams
2. New: drop the associated Timeplus Task — `DROP TASK IF EXISTS user_{sanitised_name}`

### 7. Pause / Resume

No new API needed. Reuse existing `TaskManager.pause_task()` / `resume_task()`. A paused Timeplus Task stops firing triggers; the long-running agents remain alive and idle. Resuming re-enables triggers on the next scheduled interval.

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Trigger fires while busy | API returns 409; UDF logs and discards; next scheduled fire handles it |
| Worker crashes mid-run | Manager times out (per `default_agent_timeout`), delivers partial result, sets `_busy=False`, returns to idle |
| Server restart mid-run | Agents recover from `checkpoint_sn`; replay unprocessed kanban messages; complete run before going idle |
| Invalid schedule expression | Rejected at `create_scheduled_project` call time; error returned to LLM tool result |
| Scheduled project deleted while running | `delete_project` cancels asyncio tasks and drops the Timeplus Task; in-flight run is aborted |
| Duplicate boot recovery spawn | Guard: skip re-spawn if asyncio task for `agent_id` already exists and is not done |

---

## Files Changed

| File | Change |
|---|---|
| `pulsebot/timeplus/setup.py` | Add `is_scheduled`, `schedule_type`, `schedule_expr`, `trigger_prompt` to `kanban_projects` DDL |
| `pulsebot/timeplus/tasks.py` | Add `create_project_interval_task()`, `create_project_cron_task()`, new UDF template |
| `pulsebot/agents/models.py` | Add `is_scheduled: bool` to `SubAgentSpec` and `ProjectState` |
| `pulsebot/agents/manager_agent.py` | Handle `trigger` msg_type; add `_busy` flag; skip cancel-to-workers when scheduled |
| `pulsebot/agents/project_manager.py` | Add `create_scheduled_project()`, `trigger_project()`, `mark_project_idle()`, `_recover_scheduled_projects()`, `_busy_projects` set |
| `pulsebot/skills/builtin/project_manager.py` | Add `create_scheduled_project` tool definition and handler |
| `pulsebot/api/server.py` | Add `POST /api/v1/projects/{project_id}/trigger` endpoint |

---

## Open Questions

None — all design decisions resolved during brainstorming.
