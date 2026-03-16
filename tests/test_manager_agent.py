# tests/test_manager_agent.py
"""Tests for ManagerAgent class."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pulsebot.agents.models import SubAgentSpec


@pytest.fixture
def manager_spec():
    return SubAgentSpec(
        name="Manager",
        agent_id="manager_proj_001",
        role="manager",
        task_description="Coordinate the project",
        project_id="proj_001",
        target_agents=[],
    )


@pytest.fixture
def worker_specs():
    return [
        SubAgentSpec(
            name="Analyst",
            task_description="Analyze",
            project_id="proj_001",
            target_agents=[],
        )
    ]


@pytest.fixture
def mock_timeplus():
    client = MagicMock()
    client.host = "localhost"
    client.port = 8463
    client.username = "default"
    client.password = ""
    client.query = MagicMock(return_value=[])
    return client


@pytest.fixture
def mock_config():
    cfg = MagicMock()
    cfg.agent.model = "claude-sonnet-4-20250514"
    cfg.agent.provider = "anthropic"
    cfg.agent.temperature = 0.7
    cfg.agent.max_tokens = 4096
    return cfg


def make_manager(manager_spec, worker_specs, mock_timeplus, mock_config, session_id="sess_001"):
    mock_llm = MagicMock()
    mock_llm.provider_name = "test"
    mock_llm.model = "test"
    mock_llm.get_tool_definitions = MagicMock(return_value=[])
    mock_skill_loader = MagicMock()
    mock_skill_loader.get_loaded_skills = MagicMock(return_value=[])
    mock_skill_loader.create_subset = MagicMock(return_value=MagicMock(
        get_tools=MagicMock(return_value=[]),
        get_loaded_skills=MagicMock(return_value=[]),
    ))
    mock_skill_loader.get_tools = MagicMock(return_value=[])
    mock_executor = MagicMock()

    from pulsebot.agents.manager_agent import ManagerAgent
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter"):
        return ManagerAgent(
            spec=manager_spec,
            worker_specs=worker_specs,
            session_id=session_id,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )


def test_manager_agent_has_messages_writer(manager_spec, worker_specs,
                                            mock_timeplus, mock_config):
    manager = make_manager(manager_spec, worker_specs, mock_timeplus, mock_config)
    assert hasattr(manager, "messages_writer")
    assert hasattr(manager, "session_id")
    assert manager.session_id == "sess_001"


@pytest.mark.asyncio
async def test_deliver_result_writes_to_messages_stream(
        manager_spec, worker_specs, mock_timeplus, mock_config):
    from pulsebot.agents.manager_agent import ManagerAgent
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter") as MockWriter:
        mock_writer = AsyncMock()
        MockWriter.return_value = mock_writer

        mock_llm = MagicMock()
        mock_llm.get_tool_definitions = MagicMock(return_value=[])
        mock_skill_loader = MagicMock()
        mock_skill_loader.get_loaded_skills = MagicMock(return_value=[])
        mock_skill_loader.get_tools = MagicMock(return_value=[])
        mock_executor = MagicMock()

        manager = ManagerAgent(
            spec=manager_spec,
            worker_specs=worker_specs,
            session_id="sess_001",
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )
        manager.messages_writer = mock_writer

        result_message = {
            "msg_id": "msg_final",
            "content": "## Final Report\n\nSummary here.",
            "sender_id": "agent_analyst",
        }
        await manager._deliver_result(result_message)

        mock_writer.write.assert_called_once()
        write_args = mock_writer.write.call_args[0][0]
        assert write_args["session_id"] == "sess_001"
        assert write_args["target"] == "user"
        assert "Final Report" in write_args["content"]
