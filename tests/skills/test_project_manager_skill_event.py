from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.mark.asyncio
async def test_create_event_driven_project_tool_calls_manager():
    """create_event_driven_project tool routes to ProjectManager.create_event_driven_project."""
    from pulsebot.skills.builtin.project_manager import ProjectManagerSkill

    mock_pm = MagicMock()
    mock_pm.create_event_driven_project = AsyncMock(return_value="proj_event_123")

    skill = ProjectManagerSkill.__new__(ProjectManagerSkill)
    skill._project_manager = mock_pm

    result = await skill._create_event_driven_project({
        "name": "Error Monitor",
        "description": "Monitors error events",
        "agents": [{"name": "analyst", "role": "Analyze errors"}],
        "session_id": "sess_abc",
        "event_query": "SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        "context_field": "payload",
        "trigger_prompt": "A system error was detected. Investigate and summarize:",
    })

    mock_pm.create_event_driven_project.assert_called_once_with(
        name="Error Monitor",
        description="Monitors error events",
        agents=[{"name": "analyst", "role": "Analyze errors"}],
        session_id="sess_abc",
        event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        context_field="payload",
        trigger_prompt="A system error was detected. Investigate and summarize:",
        initial_messages=[],
    )
    assert "proj_event_123" in result.output
    assert "Error Monitor" in result.output


def test_create_event_driven_project_tool_in_get_tools():
    from pulsebot.skills.builtin.project_manager import ProjectManagerSkill

    mock_pm = MagicMock()
    skill = ProjectManagerSkill.__new__(ProjectManagerSkill)
    skill._project_manager = mock_pm

    tools = skill.get_tools()
    names = [t.name for t in tools]
    assert "create_event_driven_project" in names
