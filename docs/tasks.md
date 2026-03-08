# Task Design: Scheduled Tasks in PulseBot

PulseBot integrates with **Timeplus native Tasks** to provide SQL-native scheduling. Tasks are first-class citizens in Timeplus (similar to a scheduled query), which means they are durable, observable, and survive agent restarts.

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│                  Timeplus Engine                        │
│                                                        │
│  ┌───────────────────────────────────────────────────┐ │
│  │  TASK user_<name>                                 │ │
│  │  SCHEDULE 15m  (interval)                         │ │
│  │  -or-                                             │ │
│  │  SCHEDULE 1m   (cron: polls every minute)         │ │
│  │                                                   │ │
│  │  INTO pulsebot.task_triggers AS                   │ │
│  │  SELECT                                           │ │
│  │    uuid()                AS trigger_id,           │ │
│  │    '<task_name>'         AS task_name,            │ │
│  │    '<prompt>'            AS prompt,               │ │
│  │    trigger_pulsebot_task(...) AS execution_id     │ │
│  │           │                                       │ │
│  │           │ HTTP POST                             │ │
│  └───────────┼───────────────────────────────────────┘ │
└──────────────┼─────────────────────────────────────────┘
               │  POST /api/v1/task-trigger
               ▼
┌─────────────────────────────┐
│       PulseBot API          │
│  (FastAPI server)           │
│                             │
│  Writes scheduled_task msg  │
│  to pulsebot.messages       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Agent Loop            │
│                             │
│  Processes with LLM         │
│  (uses task's global        │
│   session_id)               │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         NotificationDispatcher          │
│                                         │
│  Writes task_notification event to      │
│  pulsebot.events                        │
└──────┬───────────────────────┬──────────┘
       │                       │
       ▼                       ▼
┌──────────────┐     ┌──────────────────────┐
│  Telegram    │     │  WebSocket clients   │
│  Broadcast   │     │  (task_notification  │
│  (all chats) │     │   message type)      │
└──────────────┘     └──────────────────────┘
```

---

## How It Works

### 1. Task Creation

When the LLM calls `create_interval_task` or `create_cron_task`, the `SchedulerSkill` delegates to `TaskManager`, which:

1. Creates a **Timeplus Python UDF** (`trigger_pulsebot_task` or `check_cron_and_trigger`) embedded with the API server URL.
2. Creates a **Timeplus TASK** that runs on the requested schedule. The TASK's SELECT clause calls the UDF and inserts rows into `pulsebot.task_triggers`.

**Interval task** — fires on a fixed cadence (e.g., every 15 minutes):

```sql
CREATE TASK IF NOT EXISTS user_weather_report
SCHEDULE 15m
TIMEOUT 30s
INTO pulsebot.task_triggers AS
SELECT
    uuid()                                                         AS trigger_id,
    'user_weather_report'                                          AS task_id,
    'user_weather_report'                                          AS task_name,
    'Fetch the current weather for San Francisco'                  AS prompt,
    trigger_pulsebot_task('user_weather_report', 'user_weather_report',
        'Fetch the current weather for San Francisco')             AS execution_id,
    now64(3)                                                       AS triggered_at
```

**Cron task** — polls every minute; the Python UDF checks the cron expression in-process (±1 minute accuracy):

```sql
CREATE TASK IF NOT EXISTS user_morning_brief
SCHEDULE 1m
TIMEOUT 30s
INTO pulsebot.task_triggers AS
SELECT ...
    check_cron_and_trigger('user_morning_brief', 'user_morning_brief',
        'Send my morning news briefing', '0 8 * * *')  AS execution_id,
```

### 2. Trigger Callback

On each firing, the Python UDF POSTs to `/api/v1/task-trigger`:

```json
{
  "task_id": "user_weather_report",
  "task_name": "user_weather_report",
  "prompt": "Fetch the current weather for San Francisco",
  "trigger_type": "interval"
}
```

The API server writes a `scheduled_task` message to `pulsebot.messages` with `session_id = "global_task_<task_name>"`.

### 3. Agent Processing

The agent loop picks up the `scheduled_task` message and processes it with the LLM under the task's global session. The session is stable across runs, so the agent retains conversation context between executions.

### 4. Broadcast via Events Stream

After the agent produces a response, it routes the message through `NotificationDispatcher`, which writes a `task_notification` event to `pulsebot.events`:

```json
{
  "event_type": "task_notification",
  "source": "agent",
  "severity": "info",
  "payload": {
    "task_name": "user_weather_report",
    "text": "Current weather in San Francisco: 16°C, partly cloudy...",
    "session_id": "global_task_user_weather_report"
  },
  "tags": ["task", "broadcast"]
}
```

Channel adapters each subscribe independently to the events stream and fan out to their active connections.

---

## Streams Involved

| Stream | Role |
|--------|------|
| `pulsebot.tasks` | DDL-level task definitions (created by `setup.py`) |
| `pulsebot.task_triggers` | Append-only audit log of every task invocation |
| `pulsebot.messages` | `scheduled_task` messages consumed by the agent |
| `pulsebot.events` | `task_notification` events consumed by channel adapters |

---

## Scheduler Skill Tools

The `scheduler` built-in skill exposes 6 LLM-callable tools:

| Tool | Arguments | Description |
|------|-----------|-------------|
| `create_interval_task` | `name`, `prompt`, `interval` | Create a task that fires every `interval` (e.g. `15m`, `1h`) |
| `create_cron_task` | `name`, `prompt`, `cron` | Create a task on a calendar schedule (5-field cron, ±1 min accuracy) |
| `list_tasks` | — | List all user-created tasks and their status |
| `pause_task` | `name` | Stop a task from firing |
| `resume_task` | `name` | Restart a paused task |
| `delete_task` | `name` | Permanently delete a task |

> Only tasks with names starting with `user_` can be managed via these tools. Internal tasks (e.g., `heartbeat_task`) are protected.

---

## CLI Commands

```bash
# List all scheduled tasks
pulsebot task list

# Create an interval task (fires every 30 minutes)
pulsebot task create --name weather-check \
  --prompt "Fetch the current weather for San Francisco" \
  --interval 30m

# Create a cron task (fires at 8:00 AM every day)
pulsebot task create --name morning-briefing \
  --prompt "Send my morning news briefing" \
  --cron "0 8 * * *"

# Pause a task
pulsebot task pause user_weather_check

# Resume a task
pulsebot task resume user_weather_check

# Delete a task
pulsebot task delete user_weather_check
```

> **Note**: CLI `create` uses the default `workspace.api_server_url` from `config.yaml` as the UDF callback URL. Ensure this is set correctly before creating tasks.

---

## Telegram Fan-Out

The Telegram channel adapter subscribes to `pulsebot.events` and broadcasts every `task_notification` to all active Telegram chats:

- **Active sessions**: Chats that have sent at least one message to the bot in the current runtime.
- **Session restore**: On startup, the adapter reads the 100 most recent Telegram messages from history to restore the session map — task broadcasts survive agent restarts.
- **Fallback**: If no active sessions exist, it falls back to the `channels.telegram.allow_from` list.

---

## Web UI Fan-Out

Each WebSocket session subscribes to a `forward_task_notifications` coroutine that streams all `task_notification` events from `pulsebot.events`. The web UI renders these as a distinct notification banner.

WebSocket message sent to the browser:

```json
{
  "type": "task_notification",
  "task_name": "user_weather_report",
  "text": "Current weather in San Francisco: 16°C, partly cloudy..."
}
```

---

## Required Permissions (Docker / Proton)

The `pulsebot` database user needs the following privileges to create and manage tasks:

```sql
GRANT CREATE FUNCTION ON *.* TO pulsebot;
GRANT DROP FUNCTION ON *.* TO pulsebot;
GRANT SHOW FUNCTIONS ON *.* TO pulsebot;
GRANT CREATE TASK ON *.* TO pulsebot;
GRANT DROP TASK ON *.* TO pulsebot;
GRANT SHOW TASKS ON *.* TO pulsebot;
```

These are automatically granted by `docker/start-all-in-one.sh` for both Proton and Timeplus Enterprise images.

---

## Task Naming

All user-created tasks are automatically sanitised and prefixed with `user_`:

- Input name: `"Weather Report"` → internal name: `user_weather_report`
- Only lower-case alphanumerics and underscores are kept; other characters are replaced by `_`.

This prefix ensures user tasks cannot accidentally overlap with internal system tasks.

---

## Cron Accuracy

Cron tasks poll every **1 minute** using a standard Timeplus TASK with `SCHEDULE 1m`. The Python UDF checks the cron expression in-process each minute using the server's local time. Accuracy is **±1 minute** relative to wall-clock time.

Standard 5-field cron expressions are supported:

```
┌─── minute (0-59)
│  ┌─── hour (0-23)
│  │  ┌─── day of month (1-31)
│  │  │  ┌─── month (1-12)
│  │  │  │  ┌─── day of week (0-6, Monday=0)
│  │  │  │  │
*  *  *  *  *
```

Examples:

| Expression | Meaning |
|------------|---------|
| `0 8 * * *` | Every day at 8:00 AM |
| `*/15 * * * *` | Every 15 minutes |
| `0 9 * * 1` | Every Monday at 9:00 AM |
| `0 18 * * 1-5` | Weekdays at 6:00 PM |
