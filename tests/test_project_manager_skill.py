"""Tests for the project_manager built-in skill."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from pulsebot.agents.models import ProjectState  # noqa: E402


@pytest.fixture
def mock_project_state():
    return ProjectState(
        project_id="proj_abc123",
        name="Test",
        description="Test project",
        session_id="sess_001",
        agent_ids=["manager_proj_abc123", "agent_researcher"],
        status="active",
        created_by="sess_001",
    )


@pytest.fixture
def mock_pm(mock_project_state):
    pm = MagicMock()
    pm.create_project = AsyncMock(return_value="proj_abc123")
    pm.list_projects = MagicMock(return_value=[mock_project_state])
    pm.cancel_project = AsyncMock(return_value=True)
    pm.get_project_status = MagicMock(return_value=mock_project_state)
    return pm


@pytest.fixture
def skill(mock_pm):
    from pulsebot.skills.builtin.project_manager import ProjectManagerSkill
    return ProjectManagerSkill(project_manager=mock_pm)


def test_project_manager_skill_has_required_tools(skill):
    tool_names = {t.name for t in skill.get_tools()}
    assert "create_project" in tool_names
    assert "list_projects" in tool_names
    assert "cancel_project" in tool_names
    assert "get_project_status" in tool_names


@pytest.mark.asyncio
async def test_create_project_tool_calls_project_manager(skill, mock_pm):
    result = await skill.execute("create_project", {
        "name": "Market Research",
        "description": "Research AI market",
        "agents": [
            {
                "name": "Researcher",
                "task_description": "Research things",
                "target_agents": [],
            }
        ],
        "session_id": "sess_001",
        "initial_messages": [],
    })
    assert result.success is True
    assert "proj_abc123" in result.output
    mock_pm.create_project.assert_called_once()


@pytest.mark.asyncio
async def test_list_projects_tool(skill, mock_pm):
    result = await skill.execute("list_projects", {})
    assert result.success is True
    assert "proj_abc123" in result.output


@pytest.mark.asyncio
async def test_cancel_project_tool(skill, mock_pm):
    result = await skill.execute("cancel_project", {"project_id": "proj_abc123"})
    assert result.success is True
    mock_pm.cancel_project.assert_called_once_with("proj_abc123")


@pytest.mark.asyncio
async def test_get_project_status_tool(skill, mock_pm):
    result = await skill.execute("get_project_status", {"project_id": "proj_abc123"})
    assert result.success is True
    assert "proj_abc123" in result.output


@pytest.mark.asyncio
async def test_unknown_tool_returns_failure(skill):
    result = await skill.execute("nonexistent_tool", {})
    assert result.success is False
