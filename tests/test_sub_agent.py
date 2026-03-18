"""Tests for SubAgent class."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pulsebot.agents.models import SubAgentSpec
from pulsebot.agents.sub_agent import SubAgent
from pulsebot.providers.base import LLMResponse, Usage


@pytest.fixture
def spec():
    return SubAgentSpec(
        name="Analyst",
        task_description="Analyze things",
        project_id="proj_001",
        target_agents=[],
    )


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
def mock_llm():
    provider = MagicMock()
    provider.provider_name = "test"
    provider.model = "test-model"
    provider.get_tool_definitions = MagicMock(return_value=[])
    provider.chat = AsyncMock(return_value=LLMResponse(
        content="Analysis complete.",
        tool_calls=None,
        usage=Usage(input_tokens=10, output_tokens=5),
    ))
    return provider


@pytest.fixture
def mock_skill_loader():
    loader = MagicMock()
    loader.get_loaded_skills = MagicMock(return_value=[])
    loader.create_subset = MagicMock(return_value=MagicMock(
        get_tools=MagicMock(return_value=[]),
        get_loaded_skills=MagicMock(return_value=[]),
    ))
    loader.get_tools = MagicMock(return_value=[])
    return loader


@pytest.fixture
def mock_executor():
    executor = MagicMock()
    executor.execute = AsyncMock(return_value={"success": True, "output": "done", "error": ""})
    return executor


@pytest.fixture
def mock_config():
    config = MagicMock()
    config.agent.model = "claude-sonnet-4-20250514"
    config.agent.provider = "anthropic"
    config.agent.temperature = 0.7
    config.agent.max_tokens = 4096
    return config


def make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.timeplus.client.TimeplusClient", return_value=MagicMock()):
        return SubAgent(
            spec=spec,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )


def test_sub_agent_agent_id_from_spec(spec, mock_timeplus, mock_llm,
                                       mock_skill_loader, mock_executor, mock_config):
    agent = make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader,
                       mock_executor, mock_config)
    assert agent.agent_id == "agent_analyst"
    assert agent.project_id == "proj_001"


def test_sub_agent_inherits_all_skills_when_spec_skills_is_none(
        spec, mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    """When spec.skills is None, SubAgent uses the full parent skill_loader."""
    make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader,
               mock_executor, mock_config)
    # create_subset should NOT have been called (inherited all)
    mock_skill_loader.create_subset.assert_not_called()


def test_sub_agent_creates_subset_when_skills_specified(
        mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    spec = SubAgentSpec(
        name="Shell Worker",
        task_description="Run commands",
        project_id="proj_001",
        target_agents=[],
        skills=["shell"],
    )
    make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader,
               mock_executor, mock_config)
    mock_skill_loader.create_subset.assert_called_once_with(["shell"])


@pytest.mark.asyncio
async def test_process_task_calls_llm_and_writes_to_kanban(
        spec, mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    mock_batch = MagicMock()
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.timeplus.client.TimeplusClient", return_value=mock_batch):
        agent = SubAgent(
            spec=spec,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )

        message = {
            "msg_id": "msg_001",
            "project_id": "proj_001",
            "sender_id": "manager_proj_001",
            "target_id": "agent_analyst",
            "msg_type": "task",
            "content": "Analyze the data",
            "_tp_sn": 42,
        }

        await agent._process_task(message)

        # LLM should have been called
        mock_llm.chat.assert_called_once()

        # Result should have been written to kanban via client.insert
        mock_batch.insert.assert_called()
        call_args = mock_batch.insert.call_args
        stream_name = call_args[0][0]
        row = call_args[0][1][0]
        assert stream_name == "pulsebot.kanban"
        assert row["msg_type"] == "result"
        assert row["sender_id"] == "agent_analyst"
        assert row["content"] == "Analysis complete."


@pytest.mark.asyncio
async def test_process_task_routes_to_target_agents(
        mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    spec = SubAgentSpec(
        name="Researcher",
        task_description="Research",
        project_id="proj_001",
        target_agents=["agent_analyst"],
    )
    mock_batch = MagicMock()
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.timeplus.client.TimeplusClient", return_value=mock_batch):
        agent = SubAgent(
            spec=spec,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )

        message = {
            "msg_id": "msg_001",
            "project_id": "proj_001",
            "sender_id": "manager_proj_001",
            "target_id": "agent_researcher",
            "msg_type": "task",
            "content": "Research AI",
            "_tp_sn": 1,
        }
        await agent._process_task(message)

        call_args = mock_batch.insert.call_args
        row = call_args[0][1][0]
        assert row["target_id"] == "agent_analyst"
        # Routing to another worker (not manager) must use msg_type="task"
        # so the recipient's kanban listener (which filters 'task','control') picks it up.
        assert row["msg_type"] == "task"


@pytest.mark.asyncio
async def test_process_task_uses_result_msg_type_for_manager(
        mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    """When target_agents is empty the result goes to the manager with msg_type='result'."""
    spec = SubAgentSpec(
        name="Analyst",
        task_description="Analyse",
        project_id="proj_001",
        target_agents=[],  # falls back to manager
    )
    mock_batch = MagicMock()
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.timeplus.client.TimeplusClient", return_value=mock_batch):
        agent = SubAgent(
            spec=spec,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )

        message = {
            "msg_id": "msg_002",
            "project_id": "proj_001",
            "sender_id": "manager_proj_001",
            "target_id": "agent_analyst",
            "msg_type": "task",
            "content": "Analyse data",
            "_tp_sn": 2,
        }
        await agent._process_task(message)

        call_args = mock_batch.insert.call_args
        row = call_args[0][1][0]
        assert row["target_id"] == "manager_proj_001"
        assert row["msg_type"] == "result"
