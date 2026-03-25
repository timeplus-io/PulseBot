"""Tests for ProjectManager event-driven project methods."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

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
    import json
    parsed_content = json.loads(row["content"])
    assert parsed_content == {"prompt": "Do:\n\nevent data"}


def test_trigger_project_with_context_returns_false_when_busy():
    pm = make_pm()
    pm._busy_projects.add("proj_1")

    result = pm.trigger_project_with_context("proj_1", "some prompt")
    assert result is False


def test_trigger_project_with_context_returns_false_for_unknown_project():
    pm = make_pm()
    result = pm.trigger_project_with_context("nonexistent", "prompt")
    assert result is False


def test_cancel_project_cancels_event_watcher():
    """cancel_project must also cancel and remove the EventWatcher task."""
    pm = make_pm()
    from unittest.mock import MagicMock

    from pulsebot.agents.models import ProjectState

    project_id = "proj_cancel_ew"
    manager_id = f"manager_{project_id}"
    worker_id = f"worker_{project_id}"
    watcher_key = f"event_watcher_{project_id}"

    pm._projects[project_id] = ProjectState(
        project_id=project_id,
        name="Event Project",
        description="",
        session_id="sess",
        agent_ids=[manager_id, worker_id],
        is_scheduled=True,
        schedule_type="event",
        trigger_prompt="Investigate:",
    )

    # Set up mock tasks for the regular agents and the EventWatcher
    manager_task = MagicMock()
    manager_task.done.return_value = False
    worker_task = MagicMock()
    worker_task.done.return_value = False
    watcher_task = MagicMock()
    watcher_task.done.return_value = False

    pm._agent_tasks[manager_id] = manager_task
    pm._agent_tasks[worker_id] = worker_task
    pm._agent_tasks[watcher_key] = watcher_task

    import asyncio
    result = asyncio.get_event_loop().run_until_complete(pm.cancel_project(project_id))

    assert result is True
    manager_task.cancel.assert_called_once()
    worker_task.cancel.assert_called_once()
    watcher_task.cancel.assert_called_once()
    # EventWatcher must be removed from _agent_tasks
    assert watcher_key not in pm._agent_tasks


def test_delete_project_cancels_event_watcher():
    """delete_project must cancel and remove the EventWatcher task (regression guard)."""
    pm = make_pm()
    from unittest.mock import MagicMock

    from pulsebot.agents.models import ProjectState

    project_id = "proj_delete_ew"
    manager_id = f"manager_{project_id}"
    watcher_key = f"event_watcher_{project_id}"

    pm._projects[project_id] = ProjectState(
        project_id=project_id,
        name="Event Project Delete",
        description="",
        session_id="sess",
        agent_ids=[manager_id],
        is_scheduled=True,
        schedule_type="event",
        trigger_prompt="Watch:",
    )

    manager_task = MagicMock()
    manager_task.done.return_value = False
    watcher_task = MagicMock()
    watcher_task.done.return_value = False

    pm._agent_tasks[manager_id] = manager_task
    pm._agent_tasks[watcher_key] = watcher_task

    import asyncio
    result = asyncio.get_event_loop().run_until_complete(pm.delete_project(project_id))

    assert result is True
    manager_task.cancel.assert_called_once()
    watcher_task.cancel.assert_called_once()
    assert watcher_key not in pm._agent_tasks


def test_write_project_metadata_accepts_event_fields():
    pm = make_pm()
    from pulsebot.agents.models import SubAgentSpec
    agent = SubAgentSpec(
        name="Worker",
        task_description="desc",
        project_id="proj_1",
        target_agents=[],
    )

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
