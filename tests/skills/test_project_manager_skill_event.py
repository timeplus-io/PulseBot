from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.mark.asyncio
async def test_create_event_driven_project_tool_calls_manager():
    """create_event_driven_project tool converts agent dicts to SubAgentSpec before calling ProjectManager."""
    from pulsebot.agents.models import SubAgentSpec
    from pulsebot.skills.builtin.project_manager import ProjectManagerSkill

    mock_pm = MagicMock()
    mock_pm.create_event_driven_project = AsyncMock(return_value="proj_event_123")

    skill = ProjectManagerSkill(mock_pm)

    result = await skill.execute("create_event_driven_project", {
        "name": "Error Monitor",
        "description": "Monitors error events",
        "agents": [{"name": "analyst", "task_description": "Analyze errors", "target_agents": []}],
        "session_id": "sess_abc",
        "event_query": "SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        "context_field": "payload",
        "trigger_prompt": "A system error was detected. Investigate and summarize:",
    })

    call_kwargs = mock_pm.create_event_driven_project.call_args.kwargs
    assert call_kwargs["name"] == "Error Monitor"
    assert call_kwargs["session_id"] == "sess_abc"
    assert call_kwargs["event_query"] == "SELECT payload FROM pulsebot.events WHERE severity = 'error'"
    assert call_kwargs["context_field"] == "payload"
    assert call_kwargs["initial_messages"] == []
    # agents must be SubAgentSpec objects, not raw dicts
    assert len(call_kwargs["agents"]) == 1
    spec = call_kwargs["agents"][0]
    assert isinstance(spec, SubAgentSpec)
    assert spec.name == "analyst"
    assert spec.task_description == "Analyze errors"
    assert "proj_event_123" in result.output
    assert "Error Monitor" in result.output


def test_create_event_driven_project_tool_in_get_tools():
    from pulsebot.skills.builtin.project_manager import ProjectManagerSkill

    mock_pm = MagicMock()
    skill = ProjectManagerSkill(mock_pm)

    tools = skill.get_tools()
    names = [t.name for t in tools]
    assert "create_event_driven_project" in names
