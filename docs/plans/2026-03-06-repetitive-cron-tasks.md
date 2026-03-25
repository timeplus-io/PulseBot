# Repetitive/Cron Task Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enable users to create repeating interval and cron-scheduled tasks via natural language; Timeplus Python UDFs invoke a PulseBot REST callback that drives the full LLM pipeline, and results are broadcast to all connected channels via the events stream.

**Architecture:** Four layers: (1) `/api/v1/task-trigger` REST endpoint receives Python UDF callbacks from Timeplus; (2) global sessions `global_task_{task_name}` isolate task context from user conversations; (3) `TaskManager.create_interval_task()` / `create_cron_task()` generate Timeplus TASKs whose SELECT queries call embedded Python UDFs; (4) `NotificationDispatcher` writes `task_notification` events to the `pulsebot.events` stream; channel adapters subscribe and fan out to all active connections. Cron tasks are simulated via 1-minute interval tasks with in-UDF cron matching.

**Tech Stack:** Python 3.11+, Timeplus 3.0 (Python UDFs with `requests` pre-installed), FastAPI, asyncio, existing `TaskManager` / `SkillLoader` / `Agent` / `StreamWriter` infrastructure.

---

## Reference: Key Files

| File | Role |
|---|---|
| `pulsebot/timeplus/setup.py` | Stream DDL — add `tasks` and `task_triggers` (under `pulsebot` database) |
| `pulsebot/timeplus/tasks.py` | `TaskManager` — add `create_interval_task()` and `create_cron_task()` |
| `pulsebot/api/server.py` | FastAPI — add `POST /api/v1/task-trigger` endpoint |
| `pulsebot/core/agent.py` | Agent loop — handle `scheduled_task` via `NotificationDispatcher` |
| `pulsebot/core/notifier.py` | New: `NotificationDispatcher` writes `task_notification` to events stream |
| `pulsebot/channels/telegram.py` | Subscribe to events stream for `task_notification` |
| `pulsebot/skills/builtin/scheduler.py` | New: `SchedulerSkill` — 6 LLM-callable tools (pure builtin) |
| `pulsebot/skills/loader.py` | Register `SchedulerSkill` in `BUILTIN_SKILLS` |
| `pulsebot/factory.py` | Wire `SchedulerSkill` with timeplus config |
| `pulsebot/cli.py` | Add `task create / delete / pause / resume` CLI commands |
| `pulsebot/config.py` | Add `scheduler` to default builtin skills list |

---

## Task 1: New Timeplus streams — `pulsebot.tasks` and `pulsebot.task_triggers`

**Files:**
- Modify: `pulsebot/timeplus/setup.py`
- Test: `tests/test_setup.py` (create or add to)

### Step 1: Write the failing test

```python
# tests/test_setup.py
"""Tests for Timeplus stream setup DDL."""
from pulsebot.timeplus.setup import (
    TASKS_STREAM_DDL,
    TASK_TRIGGERS_STREAM_DDL,
)


def test_tasks_ddl_has_required_fields():
    ddl = TASKS_STREAM_DDL  # pulsebot.tasks
    for field in ("task_id", "task_name", "task_type", "prompt", "schedule",
                  "status", "created_at", "created_by"):
        assert field in ddl, f"Missing field: {field}"


def test_task_triggers_ddl_has_required_fields():
    ddl = TASK_TRIGGERS_STREAM_DDL
    for field in ("trigger_id", "task_id", "task_name", "prompt",
                  "execution_id", "triggered_at"):
        assert field in ddl, f"Missing field: {field}"


def test_create_streams_includes_new_streams(monkeypatch):
    """Verify the two new streams are set up alongside the existing ones."""
    executed = []

    class FakeClient:
        def execute(self, sql):
            executed.append(sql)

    import asyncio
    from pulsebot.timeplus.setup import create_streams
    asyncio.run(create_streams(FakeClient()))

    names = "\n".join(executed)
    assert "tasks" in names
    assert "task_triggers" in names
```

### Step 2: Run test to verify failure

```bash
uv run pytest tests/test_setup.py -v
```
Expected: `ImportError: cannot import name 'TASKS_STREAM_DDL'`

### Step 3: Add DDL constants and wire into `create_streams()`

Add after `EVENTS_STREAM_DDL` in `pulsebot/timeplus/setup.py`:

```python
TASKS_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS pulsebot.tasks (
    task_id     string DEFAULT uuid(),
    task_name   string,
    task_type   string,   -- 'interval' | 'cron'
    prompt      string,
    schedule    string,   -- e.g. '15m' or '0 8 * * *'
    status      string,   -- 'active' | 'paused' | 'deleted'
    created_at  datetime64(3) DEFAULT now64(3),
    created_by  string DEFAULT 'user'
)
SETTINGS event_time_column='created_at';
"""

TASK_TRIGGERS_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS pulsebot.task_triggers (
    trigger_id   string DEFAULT uuid(),
    task_id      string,
    task_name    string,
    prompt       string,
    execution_id string DEFAULT '',
    triggered_at datetime64(3) DEFAULT now64(3)
)
SETTINGS event_time_column='triggered_at';
"""
```

Then extend `create_streams()` streams list:

```python
streams = [
    ("messages",               MESSAGES_STREAM_DDL),
    ("llm_logs",               LLM_LOGS_STREAM_DDL),
    ("tool_logs",              TOOL_LOGS_STREAM_DDL),
    ("memory",                 MEMORY_STREAM_DDL),
    ("events",                 EVENTS_STREAM_DDL),
    ("tasks",         TASKS_STREAM_DDL),         # new
    ("task_triggers", TASK_TRIGGERS_STREAM_DDL), # new
]
```

Also update `drop_streams()` and `verify_streams()` to include the two new names.

### Step 4: Run test to verify pass

```bash
uv run pytest tests/test_setup.py -v
```
Expected: PASS

### Step 5: Commit

```bash
git add pulsebot/timeplus/setup.py tests/test_setup.py
git commit -m "feat: add tasks and task_triggers streams"
```

---

## Task 2: `/api/v1/task-trigger` REST endpoint

**Files:**
- Modify: `pulsebot/api/server.py`
- Create: `tests/test_task_trigger_endpoint.py`

### Context

This endpoint is the callback target for Timeplus Python UDFs. It receives a POST, writes a `scheduled_task` message into the messages stream with `session_id = "global_task_{task_name}"`, and returns an `execution_id` for the audit trail.

### Step 1: Write the failing tests

```python
# tests/test_task_trigger_endpoint.py
"""Tests for POST /api/v1/task-trigger endpoint."""
from __future__ import annotations
from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def app():
    from pulsebot.api.server import create_app
    from pulsebot.config import Config
    with patch("pulsebot.api.server.lifespan"):
        application = create_app()
    return application


@pytest.fixture
def mock_writer():
    writer = AsyncMock()
    writer.write = AsyncMock(return_value="exec-id-123")
    return writer


class TestTaskTriggerEndpoint:
    def test_valid_interval_trigger(self, app, mock_writer):
        import pulsebot.api.server as srv
        srv._writer = mock_writer
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.post("/api/v1/task-trigger", json={
            "task_id": "task-abc",
            "task_name": "weather_report",
            "prompt": "Get current weather",
            "trigger_type": "interval",
        })

        assert resp.status_code == 200
        body = resp.json()
        assert body["execution_id"]
        assert body["session_id"] == "global_task_weather_report"

    def test_missing_prompt_returns_422(self, app, mock_writer):
        import pulsebot.api.server as srv
        srv._writer = mock_writer
        client = TestClient(app)

        resp = client.post("/api/v1/task-trigger", json={
            "task_id": "task-abc",
            "task_name": "weather_report",
            # prompt missing
            "trigger_type": "interval",
        })
        assert resp.status_code == 422

    def test_message_written_with_correct_fields(self, app, mock_writer):
        import pulsebot.api.server as srv
        srv._writer = mock_writer
        client = TestClient(app)

        client.post("/api/v1/task-trigger", json={
            "task_id": "task-abc",
            "task_name": "my_task",
            "prompt": "Do something",
            "trigger_type": "interval",
        })

        call_args = mock_writer.write.call_args[0][0]
        assert call_args["session_id"] == "global_task_my_task"
        assert call_args["message_type"] == "scheduled_task"
        assert call_args["target"] == "agent"
        assert "Do something" in call_args["content"]
```

### Step 2: Run test to verify failure

```bash
uv run pytest tests/test_task_trigger_endpoint.py -v
```
Expected: `404 Not Found` (endpoint doesn't exist yet)

### Step 3: Add models and endpoint to `server.py`

Add to `pulsebot/api/server.py` (after the existing model classes):

```python
class TaskTriggerRequest(BaseModel):
    """Incoming callback from a Timeplus Python UDF."""
    task_id: str
    task_name: str
    prompt: str
    trigger_type: str = "interval"          # 'interval' | 'cron'
    cron_expression: str | None = None
    metadata: dict[str, Any] = {}


class TaskTriggerResponse(BaseModel):
    """Response to the Timeplus Python UDF callback."""
    execution_id: str
    session_id: str
    status: str = "triggered"
```

Add to the `router` (e.g., after the `/chat` endpoint):

```python
@router.post("/api/v1/task-trigger", response_model=TaskTriggerResponse)
async def trigger_task(request: TaskTriggerRequest) -> TaskTriggerResponse:
    """Receive a scheduled task callback from a Timeplus Python UDF.

    Writes a 'scheduled_task' message into the messages stream so the
    agent loop processes it under the task's global session.
    """
    if _writer is None:
        raise HTTPException(status_code=500, detail="Server not initialized")

    session_id = f"global_task_{request.task_name}"

    execution_id = await _writer.write({
        "source": "scheduler",
        "target": "agent",
        "session_id": session_id,
        "message_type": "scheduled_task",
        "content": json.dumps({
            "text": request.prompt,
            "task_id": request.task_id,
            "task_name": request.task_name,
            "trigger_type": request.trigger_type,
        }),
        "user_id": "system",
        "priority": 1,
    })

    logger.info(
        "Task trigger received",
        extra={"task_name": request.task_name, "session_id": session_id},
    )

    return TaskTriggerResponse(
        execution_id=execution_id,
        session_id=session_id,
    )
```

### Step 4: Run tests

```bash
uv run pytest tests/test_task_trigger_endpoint.py -v
uv run pytest -v
```
Expected: all pass

### Step 5: Commit

```bash
git add pulsebot/api/server.py tests/test_task_trigger_endpoint.py
git commit -m "feat: add POST /api/v1/task-trigger endpoint for Timeplus UDF callbacks"
```

---

## Task 3: `TaskManager.create_interval_task()` and `create_cron_task()`

**Files:**
- Modify: `pulsebot/timeplus/tasks.py`
- Create: `tests/test_tasks.py`

### Context

Both methods create Timeplus TASKs. Instead of inserting rows into the messages stream directly, the task query calls an embedded Python UDF (`trigger_pulsebot_task` for intervals, `check_cron_and_trigger` for cron) which HTTP POSTs to `/api/v1/task-trigger`. The UDF code is defined in-line in the `CREATE OR REPLACE FUNCTION` SQL that each method issues before creating the task.

The task SELECT result is written into `pulsebot.task_triggers` as an audit trail.

### Step 1: Write the failing tests

```python
# tests/test_tasks.py
"""Tests for TaskManager UDF-based task creation."""
from __future__ import annotations
from unittest.mock import MagicMock
import pytest
from pulsebot.timeplus.tasks import TaskManager


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.execute = MagicMock()
    client.query = MagicMock(return_value=[])
    return client


@pytest.fixture
def task_mgr(mock_client):
    return TaskManager(mock_client)


class TestCreateIntervalTask:
    def test_issues_two_sql_calls(self, task_mgr, mock_client):
        """Should CREATE FUNCTION then CREATE TASK."""
        task_mgr.create_interval_task(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )
        assert mock_client.execute.call_count == 2

    def test_udf_sql_contains_api_url(self, task_mgr, mock_client):
        task_mgr.create_interval_task(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )
        udf_sql = mock_client.execute.call_args_list[0][0][0]
        assert "http://localhost:8000" in udf_sql
        assert "trigger_pulsebot_task" in udf_sql

    def test_task_sql_contains_schedule_and_prompt(self, task_mgr, mock_client):
        task_mgr.create_interval_task(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        assert "15m" in task_sql
        assert "weather_report" in task_sql   # sanitised name
        assert "Get the weather" in task_sql
        assert "task_triggers" in task_sql

    def test_name_sanitised(self, task_mgr, mock_client):
        task_mgr.create_interval_task(
            name="My Task! #1",
            prompt="do stuff",
            interval="1h",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        # hyphens/special chars → underscores, prefixed with user_
        assert "user_my_task__1" in task_sql or "user_my_task_1" in task_sql

    def test_returns_sanitised_name(self, task_mgr, mock_client):
        result = task_mgr.create_interval_task(
            name="daily-report",
            prompt="...",
            interval="1h",
            api_url="http://localhost:8000",
        )
        assert result == "user_daily_report"


class TestCreateCronTask:
    def test_issues_two_sql_calls(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        assert mock_client.execute.call_count == 2

    def test_udf_contains_cron_matching(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        udf_sql = mock_client.execute.call_args_list[0][0][0]
        assert "check_cron_and_trigger" in udf_sql
        assert "matches_cron" in udf_sql

    def test_task_uses_1m_schedule(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        # Cron tasks poll every 1 minute, matching inside the UDF
        assert "1m" in task_sql

    def test_cron_expression_embedded_in_task(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        assert "0 8 * * *" in task_sql
```

### Step 2: Run test to verify failure

```bash
uv run pytest tests/test_tasks.py -v
```
Expected: `AttributeError: 'TaskManager' object has no attribute 'create_interval_task'`

### Step 3: Implement in `tasks.py`

Add after `create_cost_alert_task()` in `pulsebot/timeplus/tasks.py`:

```python
import re as _re

# Template for the Python UDF that triggers PulseBot on interval tasks
_INTERVAL_UDF_TEMPLATE = """
CREATE OR REPLACE FUNCTION trigger_pulsebot_task(
    task_id string, task_name string, prompt string
) RETURNS string LANGUAGE PYTHON AS $$
import requests

def trigger_pulsebot_task(task_id, task_name, prompt):
    try:
        resp = requests.post(
            '{api_url}/api/v1/task-trigger',
            json={{
                'task_id': task_id[0],
                'task_name': task_name[0],
                'prompt': prompt[0],
                'trigger_type': 'interval',
            }},
            timeout=10,
        )
        data = resp.json()
        return [data.get('execution_id', '')]
    except Exception as e:
        return [f'error: {{str(e)}}']
$$
"""

# Template for the Python UDF that triggers PulseBot on cron tasks
_CRON_UDF_TEMPLATE = """
CREATE OR REPLACE FUNCTION check_cron_and_trigger(
    task_id string, task_name string, prompt string, cron_expr string
) RETURNS string LANGUAGE PYTHON AS $$
from datetime import datetime

def _matches_field(field, value):
    if field == '*':
        return True
    for part in field.split(','):
        if '/' in part:
            base, step = part.split('/', 1)
            start = 0 if base == '*' else int(base)
            if value >= start and (value - start) % int(step) == 0:
                return True
        elif '-' in part:
            lo, hi = part.split('-', 1)
            if int(lo) <= value <= int(hi):
                return True
        elif int(part) == value:
            return True
    return False

def _matches_cron(expr, now):
    parts = expr.split()
    if len(parts) != 5:
        return False
    minute, hour, dom, month, dow = parts
    return (
        _matches_field(minute, now.minute) and
        _matches_field(hour, now.hour) and
        _matches_field(dom, now.day) and
        _matches_field(month, now.month) and
        _matches_field(dow, now.weekday())
    )

def check_cron_and_trigger(task_id, task_name, prompt, cron_expr):
    now = datetime.now()
    if not _matches_cron(cron_expr[0], now):
        return ['skipped']
    try:
        import requests
        resp = requests.post(
            '{api_url}/api/v1/task-trigger',
            json={{
                'task_id': task_id[0],
                'task_name': task_name[0],
                'prompt': prompt[0],
                'trigger_type': 'cron',
                'cron_expression': cron_expr[0],
            }},
            timeout=10,
        )
        data = resp.json()
        return [data.get('execution_id', '')]
    except Exception as e:
        return [f'error: {{str(e)}}']
$$
"""


def _sanitise_task_name(name: str) -> str:
    """Lowercase, replace non-alnum with underscore, add 'user_' prefix."""
    safe = _re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return f"user_{safe}"


def create_interval_task(
    self,
    name: str,
    prompt: str,
    interval: str,
    api_url: str = "http://localhost:8000",
) -> str:
    """Create an interval-based task using a Timeplus Python UDF.

    The task fires on the given interval, invoking the
    ``trigger_pulsebot_task`` UDF which POSTs to the PulseBot
    ``/api/v1/task-trigger`` endpoint.

    Args:
        name: Human-readable task name (will be sanitised).
        prompt: Instruction for the agent to execute each run.
        interval: Timeplus interval string, e.g. ``"15m"`` or ``"1h"``.
        api_url: Base URL of the PulseBot API server.

    Returns:
        The sanitised internal task name.
    """
    task_name = _sanitise_task_name(name)
    safe_prompt = prompt.replace("'", "''").replace('"', '\\"')

    # 1. Create the Python UDF
    udf_sql = _INTERVAL_UDF_TEMPLATE.format(api_url=api_url)
    self.client.execute(udf_sql)

    # 2. Create the Timeplus TASK
    task_sql = f"""
        CREATE TASK IF NOT EXISTS {task_name}
        SCHEDULE {interval}
        TIMEOUT 30s
        INTO pulsebot.task_triggers
        AS
        SELECT
            uuid()                                                AS trigger_id,
            '{task_name}'                                         AS task_id,
            '{task_name}'                                         AS task_name,
            '{safe_prompt}'                                       AS prompt,
            trigger_pulsebot_task('{task_name}', '{task_name}', '{safe_prompt}') AS execution_id,
            now64(3)                                              AS triggered_at
    """
    self.client.execute(task_sql)

    logger.info("Created interval task", extra={"name": task_name, "interval": interval})
    return task_name


def create_cron_task(
    self,
    name: str,
    prompt: str,
    cron: str,
    api_url: str = "http://localhost:8000",
) -> str:
    """Create a cron-scheduled task using a 1-minute polling Timeplus Task.

    The task polls every minute and uses the ``check_cron_and_trigger``
    Python UDF to match the cron expression and conditionally POST to
    the PulseBot ``/api/v1/task-trigger`` endpoint.

    Args:
        name: Human-readable task name (will be sanitised).
        prompt: Instruction for the agent to execute each run.
        cron: Standard 5-field cron expression, e.g. ``"0 8 * * *"``.
        api_url: Base URL of the PulseBot API server.

    Returns:
        The sanitised internal task name.
    """
    task_name = _sanitise_task_name(name)
    safe_prompt = prompt.replace("'", "''").replace('"', '\\"')
    safe_cron = cron.replace("'", "''")

    # 1. Create the cron-matching Python UDF
    udf_sql = _CRON_UDF_TEMPLATE.format(api_url=api_url)
    self.client.execute(udf_sql)

    # 2. Create the 1-minute polling TASK
    task_sql = f"""
        CREATE TASK IF NOT EXISTS {task_name}
        SCHEDULE 1m
        TIMEOUT 30s
        INTO pulsebot.task_triggers
        AS
        SELECT
            uuid()                                                                AS trigger_id,
            '{task_name}'                                                         AS task_id,
            '{task_name}'                                                         AS task_name,
            '{safe_prompt}'                                                       AS prompt,
            check_cron_and_trigger('{task_name}', '{task_name}', '{safe_prompt}', '{safe_cron}') AS execution_id,
            now64(3)                                                              AS triggered_at
    """
    self.client.execute(task_sql)

    logger.info("Created cron task", extra={"name": task_name, "cron": cron})
    return task_name
```

Then bind these as instance methods (add after the class definition, before end of file):

```python
TaskManager.create_interval_task = create_interval_task
TaskManager.create_cron_task = create_cron_task
TaskManager._sanitise_task_name = staticmethod(_sanitise_task_name)
```

(Or, preferably, define them inside the class body directly.)

### Step 4: Run tests

```bash
uv run pytest tests/test_tasks.py -v
uv run pytest -v
```
Expected: all pass

### Step 5: Commit

```bash
git add pulsebot/timeplus/tasks.py tests/test_tasks.py
git commit -m "feat: add TaskManager.create_interval_task() and create_cron_task() with Python UDFs"
```

---

## Task 4: `NotificationDispatcher` + agent integration

**Files:**
- Create: `pulsebot/core/notifier.py`
- Modify: `pulsebot/core/agent.py`
- Create: `tests/test_notifier.py`

### Context

When the agent finishes processing a `scheduled_task` message, instead of calling `_send_response()` (which targets only the originating channel), it calls `NotificationDispatcher.broadcast_task_result()`, which writes a `task_notification` event to the `pulsebot.events` stream. Channel adapters (Task 5) subscribe to that stream and fan out to all their active connections.

### Step 1: Write the failing tests

```python
# tests/test_notifier.py
"""Tests for NotificationDispatcher."""
from __future__ import annotations
from unittest.mock import AsyncMock
import json
import pytest
from pulsebot.core.notifier import NotificationDispatcher


@pytest.fixture
def mock_events_writer():
    writer = AsyncMock()
    writer.write = AsyncMock(return_value="event-id-1")
    return writer


@pytest.fixture
def dispatcher(mock_events_writer):
    return NotificationDispatcher(mock_events_writer)


class TestNotificationDispatcher:
    @pytest.mark.asyncio
    async def test_broadcast_writes_to_events_stream(self, dispatcher, mock_events_writer):
        await dispatcher.broadcast_task_result(
            task_name="weather_report",
            text="Current weather: sunny",
            session_id="global_task_weather_report",
        )
        mock_events_writer.write.assert_called_once()

    @pytest.mark.asyncio
    async def test_event_type_is_task_notification(self, dispatcher, mock_events_writer):
        await dispatcher.broadcast_task_result(
            task_name="weather_report",
            text="sunny",
            session_id="global_task_weather_report",
        )
        call_data = mock_events_writer.write.call_args[0][0]
        assert call_data["event_type"] == "task_notification"

    @pytest.mark.asyncio
    async def test_payload_contains_task_name_and_text(self, dispatcher, mock_events_writer):
        await dispatcher.broadcast_task_result(
            task_name="morning_brief",
            text="Market is up 2%",
            session_id="global_task_morning_brief",
        )
        call_data = mock_events_writer.write.call_args[0][0]
        payload = json.loads(call_data["payload"])
        assert payload["task_name"] == "morning_brief"
        assert payload["text"] == "Market is up 2%"
        assert payload["session_id"] == "global_task_morning_brief"

    @pytest.mark.asyncio
    async def test_broadcast_handles_writer_failure_gracefully(self, dispatcher, mock_events_writer):
        mock_events_writer.write.side_effect = Exception("stream down")
        # Should not raise; logs warning instead
        await dispatcher.broadcast_task_result("t", "msg", "s")
```

### Step 2: Run test to verify failure

```bash
uv run pytest tests/test_notifier.py -v
```
Expected: `ModuleNotFoundError: No module named 'pulsebot.core.notifier'`

### Step 3: Create `pulsebot/core/notifier.py`

```python
"""NotificationDispatcher: writes task_notification events to the events stream."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.streams import StreamWriter

logger = get_logger(__name__)


class NotificationDispatcher:
    """Broadcasts scheduled-task results to all channels via the events stream.

    Channel adapters (Telegram, WebSocket) subscribe to the events stream and
    fan out any ``task_notification`` events to their active connections.
    """

    def __init__(self, events_writer: "StreamWriter") -> None:
        self._writer = events_writer

    async def broadcast_task_result(
        self,
        task_name: str,
        text: str,
        session_id: str,
    ) -> None:
        """Write a task_notification event for all channel adapters to pick up.

        Args:
            task_name: Sanitised internal task name.
            text: The agent's response text to broadcast.
            session_id: The global session ID for this task run.
        """
        try:
            await self._writer.write({
                "event_type": "task_notification",
                "source": "agent",
                "severity": "info",
                "payload": json.dumps({
                    "task_name": task_name,
                    "text": text,
                    "session_id": session_id,
                }),
                "tags": ["task", "broadcast"],
            })
            logger.info("Broadcast task result", extra={"task_name": task_name})
        except Exception as e:
            logger.warning(
                "NotificationDispatcher failed to write event",
                extra={"task_name": task_name, "error": str(e)},
            )
```

### Step 4: Modify `agent.py` to use `NotificationDispatcher`

**4a — Add `notifier` parameter to `__init__`** (after the existing params):

```python
from pulsebot.core.notifier import NotificationDispatcher

def __init__(
    self,
    ...
    notifier: "NotificationDispatcher | None" = None,
):
    ...
    self.notifier = notifier
```

**4b — After the LLM response loop, check message type and dispatch accordingly:**

In `_process_message()`, locate the section where the final `response_text` is available and `_send_response()` is about to be called. Replace:

```python
await self._send_response(response_text, session_id, source)
```

With:

```python
if message_type == "scheduled_task" and self.notifier:
    task_name = content_dict.get("task_name", session_id.removeprefix("global_task_"))
    await self.notifier.broadcast_task_result(
        task_name=task_name,
        text=response_text,
        session_id=session_id,
    )
else:
    await self._send_response(response_text, session_id, source)
```

(Use the exact variable names present in `agent.py`. Read the file to confirm the variable names for `message_type`, `content_dict`, `response_text`, `session_id`, and `source` before editing.)

### Step 5: Run tests

```bash
uv run pytest tests/test_notifier.py -v
uv run pytest -v
```
Expected: all pass

### Step 6: Commit

```bash
git add pulsebot/core/notifier.py pulsebot/core/agent.py tests/test_notifier.py
git commit -m "feat: add NotificationDispatcher and wire into agent for scheduled_task broadcast"
```

---

## Task 5: Channel adapters — subscribe to events stream for broadcast

**Files:**
- Modify: `pulsebot/channels/telegram.py`
- Modify: `pulsebot/api/server.py` (WebSocket `send_responses`)
- Create: `tests/test_telegram_task_broadcast.py`

### Context

Both Telegram and the WebSocket currently only subscribe to the `messages` stream filtered by their own `target` and `session_id`. We need each to additionally subscribe to `pulsebot.events` where `event_type = 'task_notification'` and push results to all their active connections.

### Step 1: Write the failing tests

```python
# tests/test_telegram_task_broadcast.py
"""Tests for Telegram channel handling task_notification events."""
from __future__ import annotations
from unittest.mock import AsyncMock, MagicMock, patch
import json
import pytest


@pytest.fixture
def channel():
    from pulsebot.channels.telegram import TelegramChannel
    with patch("pulsebot.channels.telegram.Application"):
        ch = TelegramChannel.__new__(TelegramChannel)
        ch._chat_sessions = {
            "tg_111_aaa": 111,
            "tg_222_bbb": 222,
        }
        ch._bot = AsyncMock()
        ch._bot.send_message = AsyncMock()
        return ch


class TestTelegramTaskBroadcast:
    @pytest.mark.asyncio
    async def test_broadcast_event_sends_to_all_chats(self, channel):
        payload = json.dumps({
            "task_name": "weather_report",
            "text": "Sunny today!",
            "session_id": "global_task_weather_report",
        })
        await channel._handle_task_notification(payload)

        assert channel._bot.send_message.call_count == 2
        chat_ids = {c.kwargs["chat_id"]
                    for c in channel._bot.send_message.call_args_list}
        assert chat_ids == {111, 222}

    @pytest.mark.asyncio
    async def test_broadcast_sends_correct_text(self, channel):
        payload = json.dumps({
            "task_name": "weather_report",
            "text": "Sunny today!",
            "session_id": "global_task_weather_report",
        })
        await channel._handle_task_notification(payload)

        sent_text = channel._bot.send_message.call_args_list[0].kwargs["text"]
        assert "Sunny today!" in sent_text

    @pytest.mark.asyncio
    async def test_no_active_chats_does_not_raise(self, channel):
        channel._chat_sessions = {}
        await channel._handle_task_notification(
            json.dumps({"task_name": "t", "text": "msg", "session_id": "s"})
        )
        channel._bot.send_message.assert_not_called()
```

### Step 2: Run test to verify failure

```bash
uv run pytest tests/test_telegram_task_broadcast.py -v
```
Expected: `AttributeError: 'TelegramChannel' has no attribute '_handle_task_notification'`

### Step 3: Add `_handle_task_notification()` to `TelegramChannel`

Read `pulsebot/channels/telegram.py` to understand the existing structure, then add:

```python
async def _handle_task_notification(self, payload_json: str) -> None:
    """Fan out a task_notification event to all active Telegram chats."""
    import json
    try:
        payload = json.loads(payload_json)
    except Exception:
        logger.warning("Invalid task_notification payload: %s", payload_json)
        return

    text = payload.get("text", "")
    task_name = payload.get("task_name", "")

    if not self._chat_sessions:
        logger.debug("No active Telegram chats for task broadcast: %s", task_name)
        return

    for session_id, chat_id in list(self._chat_sessions.items()):
        try:
            await self._bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            logger.warning(
                "Task broadcast failed for chat %s: %s", chat_id, e
            )
```

**Also**: In the Telegram channel's main listening loop (wherever it currently streams from `messages`), add a parallel subscription to `pulsebot.events`:

```python
# In the loop that subscribes to events stream, alongside the existing messages subscription:
events_query = """
    SELECT * FROM pulsebot.events
    WHERE event_type = 'task_notification'
    SETTINGS seek_to='latest'
"""
async for event in self._events_reader.stream(events_query):
    await self._handle_task_notification(event.get("payload", "{}"))
```

(Read `telegram.py` to see how `_listen_for_responses()` is structured and where to add the events subscription. The channel will need its own `StreamReader` for the events stream, created during `start()`.)

### Step 4: Add task_notification forwarding to WebSocket

In `pulsebot/api/server.py`, inside `websocket_chat()`, modify `send_responses()` to also subscribe to events and push task notifications to all active WebSocket connections.

Simplest approach: add a second streaming task within `websocket_chat`:

```python
async def forward_task_notifications():
    """Forward task_notification events to this WebSocket client."""
    ws_events_client = TimeplusClient.from_config(_config.timeplus)
    ws_events_reader = StreamReader(ws_events_client, "events")

    events_query = """
        SELECT * FROM pulsebot.events
        WHERE event_type = 'task_notification'
        SETTINGS seek_to='latest'
    """
    try:
        async for event in ws_events_reader.stream(events_query):
            if websocket.client_state.name != "CONNECTED":
                break
            try:
                payload = json.loads(event.get("payload", "{}"))
                await websocket.send_json({
                    "type": "task_notification",
                    "task_name": payload.get("task_name", ""),
                    "text": payload.get("text", ""),
                })
            except RuntimeError:
                break
    except Exception as e:
        logger.error("WebSocket task_notification stream error: %s", e)
```

Then add `forward_task_notifications` to the `asyncio.gather()` call.

### Step 5: Run tests

```bash
uv run pytest tests/test_telegram_task_broadcast.py -v
uv run pytest -v
```
Expected: all pass

### Step 6: Commit

```bash
git add pulsebot/channels/telegram.py pulsebot/api/server.py tests/test_telegram_task_broadcast.py
git commit -m "feat: channel adapters subscribe to events stream for task_notification broadcast"
```

---

## Task 6: `SchedulerSkill` Python builtin

**Files:**
- Create: `pulsebot/skills/builtin/scheduler.py`
- Modify: `pulsebot/skills/loader.py`
- Create: `tests/test_scheduler_skill.py`

### Step 1: Write the failing tests

```python
# tests/test_scheduler_skill.py
"""Tests for SchedulerSkill."""
from __future__ import annotations
from unittest.mock import MagicMock, AsyncMock
import pytest
from pulsebot.skills.builtin.scheduler import SchedulerSkill


@pytest.fixture
def mock_task_mgr():
    mgr = MagicMock()
    mgr.create_interval_task = MagicMock(return_value="user_weather_report")
    mgr.create_cron_task = MagicMock(return_value="user_morning_brief")
    mgr.list_tasks = MagicMock(return_value=[
        {"name": "user_weather_report", "status": "Running"},
        {"name": "heartbeat_task", "status": "Running"},  # system — filtered out
    ])
    mgr.drop_task = MagicMock()
    mgr.pause_task = MagicMock()
    mgr.resume_task = MagicMock()
    return mgr


@pytest.fixture
def skill(mock_task_mgr):
    s = SchedulerSkill.__new__(SchedulerSkill)
    s.task_manager = mock_task_mgr
    s.api_url = "http://localhost:8000"
    return s


class TestSchedulerSkillTools:
    def test_exposes_six_tools(self, skill):
        names = {t.name for t in skill.get_tools()}
        assert names == {
            "create_interval_task",
            "create_cron_task",
            "list_tasks",
            "pause_task",
            "resume_task",
            "delete_task",
        }


class TestCreateIntervalTask:
    @pytest.mark.asyncio
    async def test_success(self, skill, mock_task_mgr):
        result = await skill.execute("create_interval_task", {
            "name": "weather-report",
            "prompt": "Get the weather",
            "interval": "15m",
        })
        assert result.success
        mock_task_mgr.create_interval_task.assert_called_once_with(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )

    @pytest.mark.asyncio
    async def test_failure_returns_error(self, skill, mock_task_mgr):
        mock_task_mgr.create_interval_task.side_effect = Exception("DB error")
        result = await skill.execute("create_interval_task",
                                     {"name": "x", "prompt": "y", "interval": "1h"})
        assert not result.success
        assert "DB error" in result.error


class TestCreateCronTask:
    @pytest.mark.asyncio
    async def test_success(self, skill, mock_task_mgr):
        result = await skill.execute("create_cron_task", {
            "name": "morning-brief",
            "prompt": "Daily briefing",
            "cron": "0 8 * * *",
        })
        assert result.success
        mock_task_mgr.create_cron_task.assert_called_once_with(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )


class TestListTasks:
    @pytest.mark.asyncio
    async def test_only_user_tasks_shown(self, skill):
        result = await skill.execute("list_tasks", {})
        assert result.success
        assert "user_weather_report" in result.output
        assert "heartbeat_task" not in result.output   # system task filtered

    @pytest.mark.asyncio
    async def test_empty_list_message(self, skill, mock_task_mgr):
        mock_task_mgr.list_tasks.return_value = []
        result = await skill.execute("list_tasks", {})
        assert result.success
        assert "no" in result.output.lower()


class TestPauseResumeDelete:
    @pytest.mark.asyncio
    async def test_pause_user_task(self, skill, mock_task_mgr):
        result = await skill.execute("pause_task", {"name": "user_weather_report"})
        assert result.success
        mock_task_mgr.pause_task.assert_called_once_with("user_weather_report")

    @pytest.mark.asyncio
    async def test_resume_user_task(self, skill, mock_task_mgr):
        result = await skill.execute("resume_task", {"name": "user_weather_report"})
        assert result.success
        mock_task_mgr.resume_task.assert_called_once_with("user_weather_report")

    @pytest.mark.asyncio
    async def test_delete_user_task(self, skill, mock_task_mgr):
        result = await skill.execute("delete_task", {"name": "user_weather_report"})
        assert result.success
        mock_task_mgr.drop_task.assert_called_once_with("user_weather_report")

    @pytest.mark.asyncio
    async def test_cannot_delete_system_task(self, skill, mock_task_mgr):
        result = await skill.execute("delete_task", {"name": "heartbeat_task"})
        assert not result.success
        mock_task_mgr.drop_task.assert_not_called()

    @pytest.mark.asyncio
    async def test_cannot_pause_system_task(self, skill, mock_task_mgr):
        result = await skill.execute("pause_task", {"name": "daily_summary"})
        assert not result.success
```

### Step 2: Run to verify failure

```bash
uv run pytest tests/test_scheduler_skill.py -v
```
Expected: `ModuleNotFoundError: No module named 'pulsebot.skills.builtin.scheduler'`

### Step 3: Implement `SchedulerSkill`

Create `pulsebot/skills/builtin/scheduler.py`:

```python
"""SchedulerSkill — lets the LLM create and manage user-defined recurring tasks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.config import TimeplusConfig

logger = get_logger(__name__)


class SchedulerSkill(BaseSkill):
    """LLM-callable tools for creating and managing scheduled tasks.

    Delegates to TaskManager's UDF-based methods which create Timeplus
    TASKs that POST back to /api/v1/task-trigger on each execution.
    """

    name = "scheduler"
    description = "Create and manage user-defined recurring tasks"

    def __init__(self, timeplus_config: "TimeplusConfig", api_url: str = "http://localhost:8000"):
        from pulsebot.timeplus.client import TimeplusClient
        from pulsebot.timeplus.tasks import TaskManager
        client = TimeplusClient.from_config(timeplus_config)
        self.task_manager = TaskManager(client)
        self.api_url = api_url

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="create_interval_task",
                description=(
                    "Create a task that repeats on a fixed interval (e.g. every 15 minutes). "
                    "Use this when the user says 'every X minutes/hours' or similar."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Short task name (e.g. 'weather-report')"},
                        "prompt": {"type": "string", "description": "Instruction to execute each run"},
                        "interval": {"type": "string", "description": "Interval string, e.g. '15m', '1h', '30m'"},
                    },
                    "required": ["name", "prompt", "interval"],
                },
            ),
            ToolDefinition(
                name="create_cron_task",
                description=(
                    "Create a task on a calendar schedule (e.g. 8 AM daily). "
                    "Use this when the user specifies a time of day or day of week. "
                    "Accuracy is ±1 minute."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Short task name"},
                        "prompt": {"type": "string", "description": "Instruction to execute each run"},
                        "cron": {"type": "string", "description": "5-field cron expression, e.g. '0 8 * * *'"},
                    },
                    "required": ["name", "prompt", "cron"],
                },
            ),
            ToolDefinition(
                name="list_tasks",
                description="List all user-created scheduled tasks and their current status.",
                parameters={"type": "object", "properties": {}},
            ),
            ToolDefinition(
                name="pause_task",
                description="Pause a user-created scheduled task so it stops firing.",
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name (starts with 'user_')"},
                    },
                    "required": ["name"],
                },
            ),
            ToolDefinition(
                name="resume_task",
                description="Resume a paused user-created scheduled task.",
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name (starts with 'user_')"},
                    },
                    "required": ["name"],
                },
            ),
            ToolDefinition(
                name="delete_task",
                description="Permanently delete a user-created scheduled task.",
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name (starts with 'user_')"},
                    },
                    "required": ["name"],
                },
            ),
        ]

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        if tool_name == "create_interval_task":
            return await self._create_interval(arguments)
        if tool_name == "create_cron_task":
            return await self._create_cron(arguments)
        if tool_name == "list_tasks":
            return await self._list()
        if tool_name == "pause_task":
            return await self._lifecycle("pause", arguments)
        if tool_name == "resume_task":
            return await self._lifecycle("resume", arguments)
        if tool_name == "delete_task":
            return await self._lifecycle("delete", arguments)
        return ToolResult.fail(f"Unknown tool: {tool_name}")

    async def _create_interval(self, args: dict) -> ToolResult:
        try:
            task_name = self.task_manager.create_interval_task(
                name=args["name"],
                prompt=args["prompt"],
                interval=args["interval"],
                api_url=self.api_url,
            )
            return ToolResult.ok(
                f"Interval task '{task_name}' created. "
                f"It will run every {args['interval']} and broadcast results to all channels."
            )
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _create_cron(self, args: dict) -> ToolResult:
        try:
            task_name = self.task_manager.create_cron_task(
                name=args["name"],
                prompt=args["prompt"],
                cron=args["cron"],
                api_url=self.api_url,
            )
            return ToolResult.ok(
                f"Cron task '{task_name}' created (schedule: {args['cron']}). "
                "Results will be broadcast to all channels (±1 minute accuracy)."
            )
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _list(self) -> ToolResult:
        try:
            all_tasks = self.task_manager.list_tasks()
            user_tasks = [t for t in all_tasks if t.get("name", "").startswith("user_")]
            if not user_tasks:
                return ToolResult.ok("No user-created scheduled tasks found.")
            lines = ["User-created scheduled tasks:"]
            for t in user_tasks:
                status = t.get("status", "unknown")
                lines.append(f"  • {t['name']} ({status})")
            return ToolResult.ok("\n".join(lines))
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _lifecycle(self, action: str, args: dict) -> ToolResult:
        name = args.get("name", "")
        if not name.startswith("user_"):
            return ToolResult.fail(
                f"Cannot {action} '{name}': only user-created tasks (starting with 'user_') "
                "can be managed via this tool."
            )
        try:
            if action == "pause":
                self.task_manager.pause_task(name)
            elif action == "resume":
                self.task_manager.resume_task(name)
            elif action == "delete":
                self.task_manager.drop_task(name)
            return ToolResult.ok(f"Task '{name}' {action}d.")
        except Exception as e:
            return ToolResult.fail(str(e))
```

### Step 4: Register in `BUILTIN_SKILLS`

In `pulsebot/skills/loader.py`, add to `BUILTIN_SKILLS`:

```python
BUILTIN_SKILLS = {
    ...
    "scheduler": "pulsebot.skills.builtin.scheduler.SchedulerSkill",  # ← add
}
```

### Step 5: Run tests

```bash
uv run pytest tests/test_scheduler_skill.py -v
uv run pytest -v
```
Expected: all pass

### Step 6: Commit

```bash
git add pulsebot/skills/builtin/scheduler.py pulsebot/skills/loader.py tests/test_scheduler_skill.py
git commit -m "feat: add SchedulerSkill with create/list/pause/resume/delete tools"
```

---

## Task 7: Factory wiring + CLI commands + config

**Files:**
- Modify: `pulsebot/factory.py`
- Modify: `pulsebot/cli.py`
- Modify: `pulsebot/config.py`

### Step 1: Wire `SchedulerSkill` in `factory.py`

Read `pulsebot/factory.py` to find `create_skill_loader()` and the `skill_configs` dict. Add:

```python
"scheduler": {
    "timeplus_config": config.timeplus,
    "api_url": f"http://localhost:{config.api.port if hasattr(config, 'api') else 8000}",
},
```

Also read `factory.py` to find where `Agent` is constructed, and pass the `NotificationDispatcher`:

```python
from pulsebot.core.notifier import NotificationDispatcher
from pulsebot.timeplus.streams import StreamWriter

events_writer = StreamWriter(timeplus_client, "pulsebot.events")
notifier = NotificationDispatcher(events_writer)

agent = Agent(
    ...
    notifier=notifier,
)
```

(Adjust variable names to match what `factory.py` actually uses.)

### Step 2: Add `task create / delete / pause / resume` CLI commands

In `pulsebot/cli.py`, add to the existing `task` group:

```python
@task.command("create")
@click.option("--config", "-c", "config_file", default="config.yaml")
@click.option("--name", required=True)
@click.option("--prompt", required=True)
@click.option("--interval", default=None, help="e.g. 15m, 1h")
@click.option("--cron", default=None, help="e.g. '0 8 * * *'")
def task_create(config_file, name, prompt, interval, cron):
    """Create a user-defined scheduled task."""
    from pulsebot.config import load_config
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.tasks import TaskManager

    cfg = load_config(config_file)
    client = TimeplusClient.from_config(cfg.timeplus)
    mgr = TaskManager(client)
    try:
        if interval:
            task_name = mgr.create_interval_task(name=name, prompt=prompt, interval=interval)
        elif cron:
            task_name = mgr.create_cron_task(name=name, prompt=prompt, cron=cron)
        else:
            console.print("[red]Provide --interval or --cron[/]")
            raise SystemExit(1)
        console.print(f"[green]Created task '{task_name}'[/]")
    except Exception as e:
        console.print(f"[red]{e}[/]")
        raise SystemExit(1)


@task.command("delete")
@click.option("--config", "-c", "config_file", default="config.yaml")
@click.argument("name")
def task_delete(config_file, name):
    """Delete a scheduled task."""
    from pulsebot.config import load_config
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.tasks import TaskManager

    cfg = load_config(config_file)
    mgr = TaskManager(TimeplusClient.from_config(cfg.timeplus))
    mgr.drop_task(name)
    console.print(f"[green]Deleted '{name}'[/]")


@task.command("pause")
@click.option("--config", "-c", "config_file", default="config.yaml")
@click.argument("name")
def task_pause(config_file, name):
    """Pause a scheduled task."""
    from pulsebot.config import load_config
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.tasks import TaskManager

    cfg = load_config(config_file)
    mgr = TaskManager(TimeplusClient.from_config(cfg.timeplus))
    mgr.pause_task(name)
    console.print(f"[yellow]Paused '{name}'[/]")


@task.command("resume")
@click.option("--config", "-c", "config_file", default="config.yaml")
@click.argument("name")
def task_resume(config_file, name):
    """Resume a paused scheduled task."""
    from pulsebot.config import load_config
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.tasks import TaskManager

    cfg = load_config(config_file)
    mgr = TaskManager(TimeplusClient.from_config(cfg.timeplus))
    mgr.resume_task(name)
    console.print(f"[green]Resumed '{name}'[/]")
```

### Step 3: Add `scheduler` to default config

In `pulsebot/config.py`, find `generate_default_config()` and add `scheduler` to the builtin skills list:

```yaml
skills:
  builtin:
    - web_search
    - shell
    - workspace
    - scheduler      # ← add
```

### Step 4: Run full test suite

```bash
uv run pytest -v
```
Expected: all pass

### Step 5: Manual smoke test (requires running Timeplus + API server)

```bash
# Start API server
pulsebot serve &

# Create a 2-minute repeating task
pulsebot task create --name test-task --prompt "Say hello world" --interval 2m

# Verify it was created
pulsebot task list

# After 2 minutes: check webchat and Telegram for the broadcast
# Then clean up
pulsebot task delete user_test_task
```

### Step 6: Commit

```bash
git add pulsebot/factory.py pulsebot/cli.py pulsebot/config.py
git commit -m "feat: wire SchedulerSkill + NotificationDispatcher into factory and add task CLI commands"
```

---

## Final verification

```bash
uv run pytest -v
```
Expected: all tests pass.

End-to-end flow to verify manually:
1. Start API server and agent: `pulsebot serve` + `pulsebot run`
2. In webchat/Telegram: `"send me the current time every 2 minutes"`
3. Agent calls `create_interval_task(name="current-time", prompt="...", interval="2m")`
4. Timeplus task fires every 2 minutes → Python UDF POSTs to `/api/v1/task-trigger` → `scheduled_task` message in messages stream
5. Agent processes it under session `global_task_user_current_time` → LLM response → `NotificationDispatcher` writes `task_notification` to events stream
6. Telegram channel and WebSocket both receive the event and broadcast to all active connections
7. Ask: `"show my scheduled tasks"` → agent calls `list_tasks()` → sees `user_current_time`
8. Ask: `"stop the time task"` → agent calls `delete_task(name="user_current_time")`
