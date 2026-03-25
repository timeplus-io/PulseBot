# Event-Driven Multi-Agent Projects Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a third project type (`schedule_type='event'`) where a Proton streaming SQL query triggers agent workflows per matching row.

**Architecture:** A new `EventWatcher` asyncio class subscribes to a user-defined streaming SQL query, extracts a single context field from each row, and writes a `trigger` kanban message to `ManagerAgent` (which already handles triggers via `_run_scheduled()`). `EventWatcher` checkpoints the Proton `_tp_sn` sequence number after each row so it resumes correctly after restarts. A drop-on-busy model ensures at most one run is active at a time.

**Tech Stack:** Python asyncio, Proton streaming SQL, existing `StreamReader` / `TimeplusClient`, existing `ManagerAgent` scheduled-mode trigger path (unchanged), existing `ProjectManager` infrastructure.

**Spec:** `docs/specs/2026-03-25-event-driven-projects-design.md`

---

## File Map

| File | Action | What changes |
|------|--------|-------------|
| `pulsebot/timeplus/setup.py` | Modify | Add `event_query` and `context_field` columns to `KANBAN_PROJECTS_STREAM_DDL` |
| `pulsebot/agents/models.py` | Modify | Add `event_query: str = ""` and `context_field: str = ""` to `SubAgentSpec` and `ProjectState` |
| `pulsebot/agents/event_watcher.py` | **Create** | `EventWatcher` class — streaming query subscription, per-row logic, checkpoint, reconnect |
| `pulsebot/agents/manager_agent.py` | Modify | `_update_project_status()` must write `event_query` and `context_field` to satisfy append-only invariant |
| `pulsebot/agents/project_manager.py` | Modify | Add `create_event_driven_project()`, `trigger_project_with_context()`; extend recovery, delete, metadata write |
| `pulsebot/skills/builtin/project_manager.py` | Modify | Add `create_event_driven_project` tool definition and `_create_event_driven_project()` handler |
| `tests/agents/test_event_driven_models.py` | **Create** | Unit tests for model field additions |
| `tests/agents/test_manager_agent_event.py` | **Create** | Unit test for `_update_project_status()` event fields |
| `tests/agents/test_event_watcher.py` | **Create** | Unit tests for `EventWatcher` (query building, row processing, busy-skip) |
| `tests/agents/test_project_manager_event.py` | **Create** | Unit tests for event-driven project_manager methods |

---

## Task 1: Extend Data Models

**Files:**
- Modify: `pulsebot/timeplus/setup.py`
- Modify: `pulsebot/agents/models.py`

- [ ] **Step 1: Write failing tests for model fields**

```python
# tests/agents/test_event_driven_models.py
from pulsebot.agents.models import SubAgentSpec, ProjectState

def test_sub_agent_spec_has_event_fields():
    spec = SubAgentSpec(
        name="Test",
        task_description="desc",
        project_id="proj_1",
        target_agents=[],
    )
    assert spec.event_query == ""
    assert spec.context_field == ""

def test_sub_agent_spec_event_fields_set():
    spec = SubAgentSpec(
        name="Test",
        task_description="desc",
        project_id="proj_1",
        target_agents=[],
        event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        context_field="payload",
    )
    assert spec.event_query == "SELECT payload FROM pulsebot.events WHERE severity = 'error'"
    assert spec.context_field == "payload"

def test_project_state_has_event_fields():
    state = ProjectState(
        project_id="proj_1",
        name="Test",
        description="desc",
        session_id="sess_1",
        agent_ids=["agent_a"],
    )
    assert state.event_query == ""
    assert state.context_field == ""
```

- [ ] **Step 2: Run tests — expect ImportError or AttributeError**

```bash
cd /Users/gangtao/Code/timeplus/PulseBot
pytest tests/agents/test_event_driven_models.py -v
```
Expected: FAIL — `SubAgentSpec` and `ProjectState` have no `event_query` / `context_field`.

- [ ] **Step 3: Add fields to `SubAgentSpec` in `pulsebot/agents/models.py`**

In the "Scheduled project fields" block (after line 56, `trigger_prompt` field), add:
```python
    # Event-driven project fields — only relevant for the manager spec.
    # When schedule_type='event', the manager is triggered per matching row
    # from the streaming query rather than on a fixed schedule.
    event_query: str = ""    # complete Proton streaming SQL to subscribe to
    context_field: str = ""  # column name to extract as trigger context
```

- [ ] **Step 4: Add fields to `ProjectState` in `pulsebot/agents/models.py`**

After the `trigger_prompt` field (line 87), add:
```python
    event_query: str = ""
    context_field: str = ""
```

- [ ] **Step 5: Run tests — expect PASS**

```bash
pytest tests/agents/test_event_driven_models.py -v
```
Expected: All 3 tests PASS.

- [ ] **Step 6: Update `KANBAN_PROJECTS_STREAM_DDL` in `pulsebot/timeplus/setup.py`**

In the `KANBAN_PROJECTS_STREAM_DDL` string, after the `trigger_prompt` line, add:
```sql
    event_query     string DEFAULT '',
    context_field   string DEFAULT ''
```

The full DDL block should end as:
```sql
    is_scheduled    bool DEFAULT false,
    schedule_type   string DEFAULT '',
    schedule_expr   string DEFAULT '',
    trigger_prompt  string DEFAULT '',
    event_query     string DEFAULT '',
    context_field   string DEFAULT ''
)
SETTINGS event_time_column='timestamp';
```

> **Note:** `CREATE STREAM IF NOT EXISTS` means existing streams won't be automatically migrated. Document in a comment that `pulsebot reset` will recreate streams with new columns. Running against an existing stream, the two columns just won't exist — recovery will return empty strings, which is safe.

- [ ] **Step 7: Commit**

```bash
git add pulsebot/agents/models.py pulsebot/timeplus/setup.py tests/agents/test_event_driven_models.py
git commit -m "feat: add event_query and context_field to data models and kanban_projects DDL"
```

---

## Task 2: Update `ManagerAgent._update_project_status()`

**Files:**
- Modify: `pulsebot/agents/manager_agent.py`
- Test: `tests/agents/test_manager_agent_event.py`

This is a minimal required change to satisfy the append-only write invariant: every `kanban_projects` insert must carry all scheduling and event fields.

- [ ] **Step 1: Write the failing test**

```python
# tests/agents/test_manager_agent_event.py
"""Test that ManagerAgent status updates carry event fields."""
from __future__ import annotations
from unittest.mock import MagicMock, patch
import pytest

from pulsebot.agents.models import SubAgentSpec


def make_manager_agent(event_query="", context_field=""):
    from pulsebot.agents.manager_agent import ManagerAgent

    spec = SubAgentSpec(
        name="Manager",
        agent_id="manager_proj_1",
        role="manager",
        task_description="coord",
        project_id="proj_1",
        target_agents=[],
        skills=[],
        is_scheduled=True,
        schedule_type="event",
        trigger_prompt="Do:",
        event_query=event_query,
        context_field=context_field,
    )
    worker_spec = SubAgentSpec(
        name="Worker",
        task_description="work",
        project_id="proj_1",
        target_agents=[],
    )

    timeplus = MagicMock()
    timeplus.host = "localhost"
    timeplus.port = 8463
    timeplus.username = "default"
    timeplus.password = ""

    with patch("pulsebot.agents.sub_agent.TimeplusClient"), \
         patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter"):
        manager = ManagerAgent(
            spec=spec,
            worker_specs=[worker_spec],
            session_id="sess_1",
            timeplus=timeplus,
            llm_provider=MagicMock(),
            skill_loader=MagicMock(),
            config=MagicMock(),
        )

    manager._batch_client = MagicMock()
    return manager


@pytest.mark.asyncio
async def test_update_project_status_includes_event_fields():
    manager = make_manager_agent(
        event_query="SELECT payload FROM pulsebot.events",
        context_field="payload",
    )
    await manager._update_project_status("active")

    manager._batch_client.insert.assert_called_once()
    inserted = manager._batch_client.insert.call_args[0][1][0]
    assert inserted["event_query"] == "SELECT payload FROM pulsebot.events"
    assert inserted["context_field"] == "payload"
    assert inserted["schedule_type"] == "event"
```

- [ ] **Step 2: Run test — expect FAIL**

```bash
pytest tests/agents/test_manager_agent_event.py -v
```
Expected: FAIL — `_update_project_status()` doesn't write `event_query` / `context_field`.

- [ ] **Step 3: Update `_update_project_status()` to include event fields**

In `pulsebot/agents/manager_agent.py`, find `_update_project_status()` (around line 418). The current insert dict ends with `"trigger_prompt"`. Extend it:

```python
    async def _update_project_status(self, status: str) -> None:
        """Write a project status update to kanban_projects stream.

        All scheduling and event fields are always included so that
        LIMIT 1 BY project_id queries return consistent data regardless
        of which row is most recent.
        """
        self._batch_client.insert("pulsebot.kanban_projects", [{
            "project_id": self.project_id,
            "name": "",
            "description": "",
            "status": status,
            "created_by": "main",
            "session_id": self.session_id,
            "agent_ids": [spec.agent_id for spec in self.worker_specs],
            "is_scheduled": self.spec.is_scheduled,
            "schedule_type": self.spec.schedule_type if self.spec.is_scheduled else "",
            "schedule_expr": self.spec.schedule_expr if self.spec.is_scheduled else "",
            "trigger_prompt": self.spec.trigger_prompt if self.spec.is_scheduled else "",
            "event_query": self.spec.event_query,
            "context_field": self.spec.context_field,
        }])
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
pytest tests/agents/test_manager_agent_event.py -v
```
Expected: PASS.

- [ ] **Step 5: Verify no existing tests broke**

```bash
pytest tests/ -v -k "manager"
```
Expected: All existing manager tests PASS.

- [ ] **Step 6: Commit**

```bash
git add pulsebot/agents/manager_agent.py tests/agents/test_manager_agent_event.py
git commit -m "feat: include event_query and context_field in ManagerAgent status updates"
```

---

## Task 3: Create `EventWatcher`

**Files:**
- Create: `pulsebot/agents/event_watcher.py`
- Create: `tests/agents/test_event_watcher.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/agents/test_event_watcher.py
"""Tests for EventWatcher."""
from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from pulsebot.agents.event_watcher import EventWatcher


def make_watcher(
    project_id="proj_test",
    event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
    context_field="payload",
    trigger_prompt="Investigate:",
    checkpoint_sn=0,
):
    project_manager = MagicMock()
    project_manager.is_project_busy.return_value = False
    project_manager.trigger_project_with_context = MagicMock()

    timeplus = MagicMock()
    config = MagicMock()
    start_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    watcher = EventWatcher(
        project_id=project_id,
        event_query=event_query,
        context_field=context_field,
        trigger_prompt=trigger_prompt,
        project_manager=project_manager,
        timeplus=timeplus,
        config=config,
        checkpoint_sn=checkpoint_sn,
        start_time=start_time,
    )
    return watcher, project_manager


def test_event_watcher_initial_query_no_checkpoint():
    watcher, _ = make_watcher(checkpoint_sn=0)
    query = watcher._build_query()
    assert "SETTINGS seek_to='2026-01-01 12:00:00'" in query
    assert "_tp_sn >" not in query


def test_event_watcher_query_with_checkpoint_and_where():
    """Query that already has WHERE: must append AND _tp_sn > N."""
    watcher, _ = make_watcher(
        event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        checkpoint_sn=42,
    )
    query = watcher._build_query()
    assert "AND _tp_sn > 42" in query
    assert "seek_to='earliest'" in query


def test_event_watcher_query_with_checkpoint_no_where():
    """Query with no WHERE clause: must use WHERE _tp_sn > N (not AND)."""
    watcher, _ = make_watcher(
        event_query="SELECT payload FROM pulsebot.events",
        checkpoint_sn=42,
    )
    query = watcher._build_query()
    assert "WHERE _tp_sn > 42" in query
    assert "seek_to='earliest'" in query
    assert " AND _tp_sn" not in query


def test_event_watcher_stop_sets_running_false():
    watcher, _ = make_watcher()
    watcher._running = True
    watcher.stop()
    assert watcher._running is False


@pytest.mark.asyncio
async def test_event_watcher_triggers_when_not_busy():
    watcher, pm = make_watcher(trigger_prompt="Investigate:")
    pm.is_project_busy.return_value = False

    row = {"payload": "Connection refused", "_tp_sn": 10}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_called_once_with(
        "proj_test", "Investigate:\n\nConnection refused"
    )
    assert watcher._checkpoint_sn == 10


@pytest.mark.asyncio
async def test_event_watcher_skips_when_busy():
    watcher, pm = make_watcher()
    pm.is_project_busy.return_value = True

    row = {"payload": "some event", "_tp_sn": 5}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_not_called()
    assert watcher._checkpoint_sn == 5


@pytest.mark.asyncio
async def test_event_watcher_skips_missing_context_field():
    watcher, pm = make_watcher(context_field="payload")
    pm.is_project_busy.return_value = False

    row = {"other_field": "data", "_tp_sn": 7}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_not_called()
    assert watcher._checkpoint_sn == 7


@pytest.mark.asyncio
async def test_event_watcher_skips_empty_context_value():
    watcher, pm = make_watcher(context_field="payload")
    pm.is_project_busy.return_value = False

    row = {"payload": "", "_tp_sn": 9}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_not_called()
    assert watcher._checkpoint_sn == 9
```

- [ ] **Step 2: Run tests — expect ImportError**

```bash
pytest tests/agents/test_event_watcher.py -v
```
Expected: FAIL — `pulsebot.agents.event_watcher` does not exist.

- [ ] **Step 3: Create `pulsebot/agents/event_watcher.py`**

```python
# pulsebot/agents/event_watcher.py
"""EventWatcher: subscribes to a streaming query and triggers project runs per matching row."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from pulsebot.timeplus.streams import StreamReader
from pulsebot.timeplus.client import TimeplusClient
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.agents.project_manager import ProjectManager
    from pulsebot.config import Config
    from pulsebot.timeplus.client import TimeplusClient as TimeplusClientType

logger = get_logger(__name__)

_RECONNECT_DELAYS = [3, 10, 30]  # seconds


class EventWatcher:
    """
    Subscribes to a user-defined Proton streaming SQL query and triggers
    a project workflow once per matching row (drop-on-busy model).

    Checkpoints the Proton _tp_sn after every row so that restarts resume
    from the last processed sequence number without missing or replaying events.
    """

    def __init__(
        self,
        project_id: str,
        event_query: str,
        context_field: str,
        trigger_prompt: str,
        project_manager: ProjectManager,
        timeplus: TimeplusClientType,
        config: Config,
        checkpoint_sn: int = 0,
        start_time: datetime | None = None,
    ) -> None:
        self.project_id = project_id
        self._event_query = event_query
        self._context_field = context_field
        self._trigger_prompt = trigger_prompt
        self._pm = project_manager
        self._checkpoint_sn = checkpoint_sn
        self._start_time = start_time or datetime.now(timezone.utc)
        self._running = False

        read_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )
        batch_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )
        # StreamReader stores the client as self.client; stream_name is unused
        # when calling stream() with a raw query string.
        self._reader = StreamReader(read_client, "kanban")
        self._batch_client = batch_client

    def _build_query(self) -> str:
        """Build the streaming query with seek control and optional _tp_sn filter.

        Appends the _tp_sn filter with WHERE or AND depending on whether the
        user's event_query already contains a WHERE clause.
        """
        if self._checkpoint_sn > 0:
            has_where = "WHERE" in self._event_query.upper()
            connector = "AND" if has_where else "WHERE"
            return (
                f"{self._event_query} {connector} _tp_sn > {self._checkpoint_sn} "
                f"SETTINGS seek_to='earliest'"
            )
        seek_ts = self._start_time.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self._event_query} SETTINGS seek_to='{seek_ts}'"

    async def _persist_checkpoint(self) -> None:
        """Write the current checkpoint_sn to kanban_agents."""
        agent_id = f"event_watcher_{self.project_id}"
        try:
            self._batch_client.insert("pulsebot.kanban_agents", [{
                "agent_id": agent_id,
                "project_id": self.project_id,
                "name": "EventWatcher",
                "role": "watcher",
                "task_description": "Streaming query event watcher",
                "target_agents": [],
                "status": "running",
                "skills": [],
                "skill_overrides": "{}",
                "config": "{}",
                "checkpoint_sn": self._checkpoint_sn,
            }])
        except Exception as e:
            logger.warning(
                f"EventWatcher {self.project_id} failed to persist checkpoint "
                f"(sn={self._checkpoint_sn}): {e}"
            )

    async def _process_row(self, row: dict[str, Any]) -> None:
        """Handle one row from the streaming query."""
        sn = row.get("_tp_sn", self._checkpoint_sn)

        context_value = row.get(self._context_field, "")
        if not context_value:
            if self._context_field not in row:
                logger.warning(
                    f"EventWatcher {self.project_id}: context_field "
                    f"'{self._context_field}' not found in row — skipping"
                )
            else:
                logger.warning(
                    f"EventWatcher {self.project_id}: context_field value is empty — skipping"
                )
            self._checkpoint_sn = sn
            await self._persist_checkpoint()
            return

        if self._pm.is_project_busy(self.project_id):
            logger.debug(
                f"EventWatcher {self.project_id}: project busy — event skipped"
            )
            self._checkpoint_sn = sn
            await self._persist_checkpoint()
            return

        combined_prompt = f"{self._trigger_prompt}\n\n{context_value}"
        self._pm.trigger_project_with_context(self.project_id, combined_prompt)
        self._checkpoint_sn = sn
        await self._persist_checkpoint()
        logger.info(
            f"EventWatcher {self.project_id}: triggered run (sn={sn})"
        )

    async def run(self) -> None:
        """Main async loop: subscribe, process rows, reconnect on disconnect."""
        self._running = True
        delay_idx = 0
        logger.info(
            f"EventWatcher {self.project_id} starting "
            f"(checkpoint_sn={self._checkpoint_sn})"
        )

        while self._running:
            query = self._build_query()
            try:
                async for row in self._reader.stream(query):
                    if not self._running:
                        break
                    await self._process_row(row)
                    delay_idx = 0  # successful row resets backoff

                if self._running:
                    logger.warning(
                        f"EventWatcher {self.project_id}: streaming query ended "
                        "unexpectedly, reconnecting..."
                    )
            except Exception as e:
                if not self._running:
                    break
                delay = _RECONNECT_DELAYS[min(delay_idx, len(_RECONNECT_DELAYS) - 1)]
                logger.warning(
                    f"EventWatcher {self.project_id}: error in streaming query "
                    f"({e}), retrying in {delay}s"
                )
                await asyncio.sleep(delay)
                delay_idx += 1

        logger.info(f"EventWatcher {self.project_id} stopped")

    def stop(self) -> None:
        """Signal the run loop to exit."""
        self._running = False
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
pytest tests/agents/test_event_watcher.py -v
```
Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
git add pulsebot/agents/event_watcher.py tests/agents/test_event_watcher.py
git commit -m "feat: implement EventWatcher for event-driven project triggering"
```

---

## Task 4: Extend `ProjectManager`

**Files:**
- Modify: `pulsebot/agents/project_manager.py`
- Create: `tests/agents/test_project_manager_event.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/agents/test_project_manager_event.py
"""Tests for ProjectManager event-driven project methods."""
from __future__ import annotations
from unittest.mock import MagicMock, patch, AsyncMock
import pytest

from pulsebot.agents.project_manager import ProjectManager


def make_pm():
    """Build a minimal ProjectManager with all dependencies mocked."""
    config = MagicMock()
    config.multi_agent.max_agents_per_project = 10
    config.multi_agent.max_concurrent_projects = 5
    config.workspace.api_server_url = "http://localhost:8000"

    timeplus = MagicMock()
    timeplus.host = "localhost"
    timeplus.port = 8463
    timeplus.username = "default"
    timeplus.password = ""

    llm_provider = MagicMock()
    skill_loader = MagicMock()
    executor = MagicMock()

    with patch("pulsebot.agents.project_manager.asyncio.create_task"):
        pm = ProjectManager(
            config=config,
            timeplus=timeplus,
            llm_provider=llm_provider,
            skill_loader=skill_loader,
            executor=executor,
        )
    pm._batch_client = MagicMock()
    return pm


def test_trigger_project_with_context_marks_busy_and_inserts_trigger():
    pm = make_pm()
    from pulsebot.agents.models import ProjectState
    pm._projects["proj_1"] = ProjectState(
        project_id="proj_1",
        name="Test",
        description="",
        session_id="sess",
        agent_ids=["manager_proj_1"],
        is_scheduled=True,
        schedule_type="event",
        trigger_prompt="Do:",
    )

    result = pm.trigger_project_with_context("proj_1", "Do:\n\nevent data")

    assert result is True
    assert pm.is_project_busy("proj_1")
    pm._batch_client.insert.assert_called_once()
    call_args = pm._batch_client.insert.call_args[0]
    assert call_args[0] == "pulsebot.kanban"
    row = call_args[1][0]
    assert row["msg_type"] == "trigger"
    assert row["target_id"] == "manager_proj_1"
    assert "Do:\n\nevent data" in row["content"]


def test_trigger_project_with_context_returns_false_when_busy():
    pm = make_pm()
    pm._busy_projects.add("proj_1")

    result = pm.trigger_project_with_context("proj_1", "some prompt")
    assert result is False


def test_trigger_project_with_context_returns_false_for_unknown_project():
    pm = make_pm()
    result = pm.trigger_project_with_context("nonexistent", "prompt")
    assert result is False


def test_write_project_metadata_accepts_event_fields():
    pm = make_pm()
    from pulsebot.agents.models import SubAgentSpec
    agent = SubAgentSpec(
        name="Worker",
        task_description="desc",
        project_id="proj_1",
        target_agents=[],
    )

    # Should not raise
    pm._write_project_metadata(
        "proj_1", "Test", "desc", [agent], "sess",
        is_scheduled=True,
        schedule_type="event",
        event_query="SELECT payload FROM pulsebot.events",
        context_field="payload",
        trigger_prompt="Investigate:",
    )
    pm._batch_client.insert.assert_called_once()
    call_args = pm._batch_client.insert.call_args[0][1][0]
    assert call_args["event_query"] == "SELECT payload FROM pulsebot.events"
    assert call_args["context_field"] == "payload"
    assert call_args["schedule_type"] == "event"
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
pytest tests/agents/test_project_manager_event.py -v
```
Expected: FAIL — methods don't exist yet.

- [ ] **Step 3: Add `trigger_project_with_context()` to `ProjectManager`**

After the existing `trigger_project()` method in `project_manager.py`, add:

```python
    def trigger_project_with_context(self, project_id: str, prompt: str) -> bool:
        """Write a trigger kanban message for an event-driven project.

        Called by EventWatcher. Identical semantics to trigger_project() —
        checks busy, marks busy, writes trigger kanban message.

        Returns:
            True if trigger was sent; False if project is busy or not found.
        """
        if project_id in self._busy_projects:
            logger.info(f"Project {project_id} is busy, event trigger skipped")
            return False

        state = self._projects.get(project_id)
        if state is None:
            return False

        self._busy_projects.add(project_id)

        manager_id = f"manager_{project_id}"
        self._batch_client.insert("pulsebot.kanban", [{
            "project_id": project_id,
            "sender_id": "event_watcher",
            "target_id": manager_id,
            "msg_type": "trigger",
            "content": json.dumps({"prompt": prompt, "project_id": project_id}),
        }])

        logger.info(
            f"Event trigger sent to project {project_id}",
            extra={"project_id": project_id, "manager_id": manager_id},
        )
        return True
```

- [ ] **Step 4: Extend `_write_project_metadata()` signature**

Find `_write_project_metadata()` in `project_manager.py` (around line 390). Extend its signature with two new optional parameters and include them in the insert:

```python
    def _write_project_metadata(
        self,
        project_id: str,
        name: str,
        description: str,
        agents: list[SubAgentSpec],
        session_id: str,
        is_scheduled: bool = False,
        schedule_type: str = "",
        schedule_expr: str = "",
        trigger_prompt: str = "",
        event_query: str = "",
        context_field: str = "",
    ) -> None:
        self._batch_client.insert("pulsebot.kanban_projects", [{
            "project_id": project_id,
            "name": name,
            "description": description,
            "status": "active",
            "created_by": "main",
            "session_id": session_id,
            "agent_ids": [s.agent_id for s in agents],
            "is_scheduled": is_scheduled,
            "schedule_type": schedule_type,
            "schedule_expr": schedule_expr,
            "trigger_prompt": trigger_prompt,
            "event_query": event_query,
            "context_field": context_field,
        }])
```

- [ ] **Step 5: Run tests — expect PASS**

```bash
pytest tests/agents/test_project_manager_event.py -v
```
Expected: All tests PASS.

- [ ] **Step 6: Add `create_event_driven_project()` to `ProjectManager`**

Add this method after `create_scheduled_project()`:

```python
    async def create_event_driven_project(
        self,
        name: str,
        description: str,
        agents: list[SubAgentSpec],
        session_id: str,
        event_query: str,
        context_field: str,
        trigger_prompt: str,
        initial_messages: list[dict[str, Any]] | None = None,
    ) -> str:
        """Create an event-driven multi-agent project.

        Identical to create_scheduled_project but uses schedule_type='event',
        starts an EventWatcher asyncio task, and creates no Timeplus Task UDF.

        Args:
            name: Human-readable project name.
            description: What this project accomplishes.
            agents: Worker agent specs.
            session_id: Session for routing final output to the user.
            event_query: Complete Proton streaming SQL. Must SELECT a column
                named context_field. Must NOT use nested subqueries (FROM (...)).
            context_field: Column name in query result to extract as trigger context.
            trigger_prompt: Instruction prefix sent with each extracted context value.
            initial_messages: Optional messages dispatched once on project creation.

        Returns:
            The generated project_id.

        Raises:
            ValueError: If event_query or context_field are invalid.
        """
        if not event_query.strip():
            raise ValueError("event_query must not be empty.")
        if "FROM (" in event_query.upper():
            raise ValueError(
                "event_query must be a direct stream query; nested subqueries "
                "(FROM (...)) are not supported because _tp_sn may not propagate "
                "through subquery boundaries."
            )
        if not context_field.strip() or not context_field.isidentifier():
            raise ValueError(
                f"context_field must be a non-empty valid identifier, got: '{context_field}'"
            )

        max_agents = self.config.multi_agent.max_agents_per_project
        if len(agents) > max_agents:
            raise ValueError(f"Too many agents: {len(agents)} > max {max_agents}")
        max_projects = self.config.multi_agent.max_concurrent_projects
        active = sum(1 for p in self._projects.values() if p.status == "active")
        if active >= max_projects:
            raise ValueError(
                f"Too many concurrent projects: {active} >= max {max_projects}"
            )

        project_id = f"proj_{uuid.uuid4().hex[:12]}"
        manager_id = f"manager_{project_id}"
        initial_messages = initial_messages or []

        for spec in agents:
            spec.project_id = project_id
            spec.is_scheduled = True

        name_to_id = {spec.name: spec.agent_id for spec in agents}
        name_to_id["Manager"] = manager_id
        name_to_id["manager"] = manager_id
        for spec in agents:
            spec.target_agents = [name_to_id.get(t, t) for t in spec.target_agents]

        upstream: dict[str, list[str]] = {spec.agent_id: [] for spec in agents}
        for spec in agents:
            for target_id in spec.target_agents:
                if target_id in upstream:
                    upstream[target_id].append(spec.agent_id)
        for spec in agents:
            spec.upstream_agent_ids = upstream[spec.agent_id]

        reporting_agent_ids = [
            spec.agent_id for spec in agents
            if not spec.target_agents or manager_id in spec.target_agents
        ]

        manager_spec = SubAgentSpec(
            name="Manager",
            agent_id=manager_id,
            role="manager",
            task_description=(
                "You are the project manager for an event-driven recurring project. "
                "Coordinate worker agents, collect their results, and deliver "
                "the final output. You are triggered by real-time streaming events."
            ),
            project_id=project_id,
            target_agents=[],
            skills=[],
            is_scheduled=True,
            schedule_type="event",
            schedule_expr="",
            trigger_prompt=trigger_prompt,
            event_query=event_query,
            context_field=context_field,
        )

        self._write_project_metadata(
            project_id, name, description, agents, session_id,
            is_scheduled=True,
            schedule_type="event",
            trigger_prompt=trigger_prompt,
            event_query=event_query,
            context_field=context_field,
        )
        for spec in [manager_spec] + agents:
            self._write_agent_metadata(spec)

        state = ProjectState(
            project_id=project_id,
            name=name,
            description=description,
            session_id=session_id,
            agent_ids=[manager_id] + [spec.agent_id for spec in agents],
            is_scheduled=True,
            schedule_type="event",
            trigger_prompt=trigger_prompt,
            event_query=event_query,
            context_field=context_field,
        )
        self._projects[project_id] = state

        manager = ManagerAgent(
            spec=manager_spec,
            worker_specs=agents,
            session_id=session_id,
            timeplus=self.timeplus,
            llm_provider=self.llm,
            skill_loader=self.skills,
            config=self.config,
            initial_messages=initial_messages,
            reporting_agent_ids=reporting_agent_ids,
            on_run_complete=lambda: self.mark_project_idle(project_id),
        )
        self._agent_tasks[manager_id] = asyncio.create_task(
            manager.run(), name=f"manager_{project_id}"
        )

        for spec in agents:
            agent = SubAgent(
                spec=spec,
                timeplus=self.timeplus,
                llm_provider=self.llm,
                skill_loader=self.skills,
                config=self.config,
            )
            self._agent_tasks[spec.agent_id] = asyncio.create_task(
                agent.run(), name=spec.agent_id
            )

        # Start EventWatcher
        from pulsebot.agents.event_watcher import EventWatcher
        from datetime import datetime, timezone
        watcher = EventWatcher(
            project_id=project_id,
            event_query=event_query,
            context_field=context_field,
            trigger_prompt=trigger_prompt,
            project_manager=self,
            timeplus=self.timeplus,
            config=self.config,
            checkpoint_sn=0,
            start_time=datetime.now(timezone.utc),
        )
        watcher_task = asyncio.create_task(
            watcher.run(), name=f"event_watcher_{project_id}"
        )
        self._agent_tasks[f"event_watcher_{project_id}"] = watcher_task

        logger.info(
            f"Event-driven project {project_id} created",
            extra={"project_id": project_id, "session_id": session_id},
        )
        return project_id
```

- [ ] **Step 7: Extend `_recover_project()` to handle `schedule_type='event'`**

In `_recover_scheduled_projects()`, extend the SELECT list:

```python
            rows = self._batch_client.query("""
                SELECT project_id, name, description, session_id,
                       schedule_type, schedule_expr, trigger_prompt, agent_ids,
                       event_query, context_field
                FROM table(pulsebot.kanban_projects)
                WHERE is_scheduled = true AND status = 'active'
                ORDER BY timestamp DESC
                LIMIT 1 BY project_id
            """)
```

In `_recover_project()`, after reading `trigger_prompt` from `row`, also read:

```python
        event_query = row.get("event_query", "")
        context_field = row.get("context_field", "")
```

Then branch on `schedule_type` at the end of `_recover_project()`, after spawning manager and workers. Currently it unconditionally passes through — add event-driven path:

```python
        # For event-driven projects, start an EventWatcher instead of relying
        # on Timeplus Task UDFs.
        if schedule_type == "event":
            from pulsebot.agents.event_watcher import EventWatcher
            from datetime import datetime, timezone

            # Load EventWatcher checkpoint
            watcher_agent_id = f"event_watcher_{project_id}"
            try:
                watcher_rows = self._batch_client.query(f"""
                    SELECT checkpoint_sn
                    FROM table(pulsebot.kanban_agents)
                    WHERE agent_id = '{escape_sql_str(watcher_agent_id)}'
                    ORDER BY timestamp DESC LIMIT 1
                """)
                watcher_checkpoint = watcher_rows[0]["checkpoint_sn"] if watcher_rows else 0
            except Exception as e:
                logger.warning(
                    f"Could not load EventWatcher checkpoint for {project_id}: {e}"
                )
                watcher_checkpoint = 0

            if watcher_agent_id not in self._agent_tasks or self._agent_tasks[watcher_agent_id].done():
                watcher = EventWatcher(
                    project_id=project_id,
                    event_query=event_query,
                    context_field=context_field,
                    trigger_prompt=trigger_prompt,
                    project_manager=self,
                    timeplus=self.timeplus,
                    config=self.config,
                    checkpoint_sn=watcher_checkpoint,
                    start_time=datetime.now(timezone.utc),
                )
                self._agent_tasks[watcher_agent_id] = asyncio.create_task(
                    watcher.run(), name=watcher_agent_id
                )
                logger.info(
                    f"Recovered EventWatcher for project {project_id} "
                    f"(checkpoint_sn={watcher_checkpoint})"
                )
```

Also pass `event_query` and `context_field` when building `ProjectState`, `manager_spec`, and the inner `_build_spec()` closure inside `_recover_project()`.

For `_build_spec()` (builds worker SubAgentSpecs), add these two fields after `is_scheduled=True`:
```python
                event_query=event_query,
                context_field=context_field,
```

For `manager_spec` and `state`, add similarly:

In `state = ProjectState(...)`, add:
```python
            event_query=event_query,
            context_field=context_field,
```

In `manager_spec = SubAgentSpec(...)`, add:
```python
            event_query=event_query,
            context_field=context_field,
```

- [ ] **Step 8: Guard Timeplus Task drop in `delete_project()` for event-driven projects**

Find the Timeplus Task drop block in `delete_project()` (around line 341):

```python
        # Drop associated Timeplus Task for scheduled projects
        if state is not None and state.is_scheduled:
```

Change to only drop for interval/cron (not event):

```python
        # Drop associated Timeplus Task (only for interval/cron; event-driven use EventWatcher)
        if state is not None and state.schedule_type in ("interval", "cron"):
```

Also, cancel the EventWatcher task for event-driven projects in `delete_project()`:

After the block that cancels agent tasks (`for agent_id in state.agent_ids`), add:

```python
        # Cancel EventWatcher for event-driven projects
        if state is not None and state.schedule_type == "event":
            watcher_key = f"event_watcher_{project_id}"
            watcher_task = self._agent_tasks.pop(watcher_key, None)
            if watcher_task and not watcher_task.done():
                watcher_task.cancel()
```

- [ ] **Step 9: Run all tests**

```bash
pytest tests/agents/ -v
```
Expected: All tests PASS.

- [ ] **Step 10: Commit**

```bash
git add pulsebot/agents/project_manager.py tests/agents/test_project_manager_event.py
git commit -m "feat: add create_event_driven_project, trigger_project_with_context, recovery, and delete support"
```

---

## Task 5: Add LLM Tool to `ProjectManagerSkill`

**Files:**
- Modify: `pulsebot/skills/builtin/project_manager.py`

- [ ] **Step 1: Add tool definition to `get_tools()`**

At the end of the `return [...]` list in `get_tools()`, add a new `ToolDefinition`:

```python
            ToolDefinition(
                name="create_event_driven_project",
                description=(
                    "Create an event-driven multi-agent project that runs once per matching row "
                    "from a Proton streaming SQL query. The extracted context field value is "
                    "appended to the trigger_prompt and delivered to worker agents. At most one "
                    "run executes at a time — events arriving while a run is active are skipped. "
                    "Use for real-time alert handling, anomaly response, or any workflow that "
                    "should react immediately to streaming data (e.g. trigger on every error event)."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Short human-readable project name",
                        },
                        "description": {
                            "type": "string",
                            "description": "What this project aims to accomplish",
                        },
                        "agents": {
                            "type": "array",
                            "description": "Worker agent specifications",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Agent name"},
                                    "task_description": {"type": "string", "description": "System-level role instructions"},
                                    "target_agents": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Agent IDs that receive this agent's output. Empty = send to manager.",
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Skill names to load. Omit to inherit all main agent skills.",
                                    },
                                    "builtin_skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Builtin skills always available to this agent.",
                                    },
                                    "model": {"type": "string", "description": "Override LLM model"},
                                    "provider": {"type": "string", "description": "Override LLM provider"},
                                },
                                "required": ["name", "task_description", "target_agents"],
                            },
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Current user session ID (for routing results back to user)",
                        },
                        "event_query": {
                            "type": "string",
                            "description": (
                                "Complete Proton streaming SQL query. Must SELECT the context_field column. "
                                "Must be a direct stream query — nested subqueries (FROM (...)) are not supported. "
                                "Example: \"SELECT payload FROM pulsebot.events WHERE severity = 'error'\""
                            ),
                        },
                        "context_field": {
                            "type": "string",
                            "description": (
                                "Column name in the query result to extract as trigger context. "
                                "Its value is appended to trigger_prompt as the combined prompt for agents."
                            ),
                        },
                        "trigger_prompt": {
                            "type": "string",
                            "description": (
                                "Instruction prefix for each run. Combined with the extracted context value as "
                                "'{trigger_prompt}\\n\\n{context_value}' and sent to worker agents."
                            ),
                        },
                        "initial_messages": {
                            "type": "array",
                            "description": "Optional task messages dispatched once on project creation",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string"},
                                    "content": {"type": "string"},
                                },
                                "required": ["target", "content"],
                            },
                        },
                    },
                    "required": ["name", "description", "agents", "session_id", "event_query", "context_field", "trigger_prompt"],
                },
            ),
```

- [ ] **Step 2: Add dispatch case in `execute()`**

In the `execute()` method, add:
```python
            elif tool_name == "create_event_driven_project":
                return await self._create_event_driven_project(arguments)
```

- [ ] **Step 3: Add `_create_event_driven_project()` handler method**

After `_create_scheduled_project()`, add:

```python
    async def _create_event_driven_project(self, args: dict) -> ToolResult:
        from pulsebot.agents.models import SubAgentSpec

        raw_agents = args.get("agents", [])
        specs = [
            SubAgentSpec(
                name=a["name"],
                task_description=a["task_description"],
                project_id="",  # set by ProjectManager
                target_agents=a.get("target_agents", []),
                skills=a.get("skills"),
                builtin_skills=a.get("builtin_skills"),
                model=a.get("model"),
                provider=a.get("provider"),
            )
            for a in raw_agents
        ]

        project_id = await self._pm.create_event_driven_project(
            name=args["name"],
            description=args["description"],
            agents=specs,
            session_id=args["session_id"],
            event_query=args["event_query"],
            context_field=args["context_field"],
            trigger_prompt=args["trigger_prompt"],
            initial_messages=args.get("initial_messages", []),
        )
        return ToolResult.ok(
            f"Event-driven project created: {project_id}\n"
            f"Spawned {len(specs)} worker agent(s) listening for events from: "
            f"{args['event_query'][:80]}{'...' if len(args['event_query']) > 80 else ''}. "
            f"Agents trigger once per matching row (drop-on-busy)."
        )
```

- [ ] **Step 4: Verify skill file is valid Python**

```bash
python -c "from pulsebot.skills.builtin.project_manager import ProjectManagerSkill; print('OK')"
```
Expected: `OK`

- [ ] **Step 5: Run all tests**

```bash
pytest tests/ -v
```
Expected: All tests PASS.

- [ ] **Step 6: Commit**

```bash
git add pulsebot/skills/builtin/project_manager.py
git commit -m "feat: add create_event_driven_project LLM tool to ProjectManagerSkill"
```

---

## Task 6: Integration Smoke Test

**Goal:** Manually verify the full flow works end-to-end in a running Docker environment.

- [ ] **Step 1: Rebuild and restart**

```bash
cd pulsebot_ui && npm run build && cd ..
docker compose up -d --build
```

- [ ] **Step 2: Verify streams have new columns**

In Proton console or via `pulsebot chat`:
```sql
DESCRIBE pulsebot.kanban_projects
```
Expected: `event_query string` and `context_field string` columns present.

> **Note:** If the stream already exists without the new columns, run `pulsebot reset` to drop and recreate all streams (this deletes all data).

- [ ] **Step 3: Create an event-driven project via chat**

In chat, ask the agent to create an event-driven project using the new tool. Example prompt:
```
Create an event-driven project called "Error Monitor" that watches for error events.
Use the query: SELECT payload FROM pulsebot.events WHERE severity = 'error'
Context field: payload
Trigger prompt: A system error was detected. Summarize it briefly:
One worker agent named "Summarizer" with task: Summarize the error event in 2 sentences.
```

- [ ] **Step 4: Insert a test event and verify trigger**

```sql
INSERT INTO pulsebot.events (event_type, source, severity, payload, tags)
VALUES ('test.error', 'smoke-test', 'error', '{"message": "Connection refused on port 8463"}', ['test'])
```

Expected: Within a few seconds, the agent workflow runs and a summary appears in chat via `task_notification`.

- [ ] **Step 5: Verify checkpoint persisted**

```sql
SELECT agent_id, checkpoint_sn FROM table(pulsebot.kanban_agents)
WHERE agent_id LIKE 'event_watcher_%'
ORDER BY timestamp DESC LIMIT 5
```
Expected: A row for `event_watcher_<project_id>` with `checkpoint_sn > 0`.

- [ ] **Step 6: Restart and verify recovery**

```bash
docker compose restart pulsebot-agent
```

Wait for the agent to start, then insert another test event. Expected: The workflow triggers again (from the checkpointed `_tp_sn`).

- [ ] **Step 7: Delete the project and verify cleanup**

Ask the agent: `delete project <project_id>`. Verify the `event_watcher_*` asyncio task is cancelled (no further triggers after deletion).

---

## Task 8: Final Cleanup

- [ ] **Step 1: Run full test suite**

```bash
pytest tests/ -v --tb=short
```
Expected: All tests PASS.

- [ ] **Step 2: Lint**

```bash
ruff check pulsebot/agents/event_watcher.py pulsebot/agents/project_manager.py pulsebot/agents/manager_agent.py pulsebot/agents/models.py pulsebot/skills/builtin/project_manager.py
```
Expected: No errors.

- [ ] **Step 3: Create final summary commit (if any cleanup edits)**

```bash
git add -p  # stage only intentional changes
git commit -m "chore: cleanup and lint fixes for event-driven projects"
```

---

## Summary: Files Changed

| File | Change |
|------|--------|
| `pulsebot/timeplus/setup.py` | Added `event_query` and `context_field` to `KANBAN_PROJECTS_STREAM_DDL` |
| `pulsebot/agents/models.py` | Added `event_query: str = ""`, `context_field: str = ""` to `SubAgentSpec` and `ProjectState` |
| `pulsebot/agents/event_watcher.py` | **New** — `EventWatcher` class |
| `pulsebot/agents/manager_agent.py` | `_update_project_status()` now writes `event_query` and `context_field` |
| `pulsebot/agents/project_manager.py` | Added `create_event_driven_project()`, `trigger_project_with_context()`; extended recovery SELECT, recovery dispatch, `_write_project_metadata()` signature, `delete_project()` Timeplus Task guard and EventWatcher cancellation |
| `pulsebot/skills/builtin/project_manager.py` | Added `create_event_driven_project` tool definition and `_create_event_driven_project()` handler |
| `tests/agents/test_event_driven_models.py` | **New** — model field tests |
| `tests/agents/test_manager_agent_event.py` | **New** — `ManagerAgent._update_project_status()` event fields test |
| `tests/agents/test_event_watcher.py` | **New** — `EventWatcher` unit tests (including WHERE vs AND `_tp_sn` logic) |
| `tests/agents/test_project_manager_event.py` | **New** — `ProjectManager` event-driven method tests |
