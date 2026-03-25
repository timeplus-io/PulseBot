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
