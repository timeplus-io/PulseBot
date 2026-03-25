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

    with patch("pulsebot.timeplus.client.TimeplusClient"), \
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
