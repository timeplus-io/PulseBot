# tests/test_project_manager.py
"""Tests for ProjectManager class."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pulsebot.agents.models import SubAgentSpec


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
    cfg.agent.model = "test-model"
    cfg.agent.provider = "anthropic"
    cfg.agent.temperature = 0.7
    cfg.agent.max_tokens = 4096
    cfg.multi_agent.max_agents_per_project = 10
    cfg.multi_agent.max_concurrent_projects = 5
    return cfg


@pytest.fixture
def worker_specs():
    return [
        SubAgentSpec(
            name="Researcher",
            task_description="Research things",
            project_id="",  # set by ProjectManager
            target_agents=[],
        ),
    ]


def make_project_manager(mock_timeplus, mock_config):
    mock_llm = MagicMock()
    mock_skill_loader = MagicMock()
    mock_skill_loader.get_loaded_skills = MagicMock(return_value=[])
    mock_skill_loader.create_subset = MagicMock(return_value=MagicMock(
        get_tools=MagicMock(return_value=[]),
        get_loaded_skills=MagicMock(return_value=[]),
    ))
    mock_skill_loader.get_tools = MagicMock(return_value=[])
    mock_executor = MagicMock()

    from pulsebot.agents.project_manager import ProjectManager
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter"), \
         patch("pulsebot.agents.project_manager.StreamWriter"):
        return ProjectManager(
            config=mock_config,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
        )


@pytest.mark.asyncio
async def test_create_project_returns_project_id(
        mock_timeplus, mock_config, worker_specs):
    pm = make_project_manager(mock_timeplus, mock_config)

    with patch("pulsebot.agents.project_manager.ManagerAgent") as MockManager, \
         patch("pulsebot.agents.project_manager.SubAgent") as MockSubAgent, \
         patch("asyncio.create_task") as mock_create_task:
        MockManager.return_value.run = AsyncMock()
        MockSubAgent.return_value.run = AsyncMock()
        mock_create_task.return_value = MagicMock()
        pm._projects_writer.write = AsyncMock()
        pm._agents_writer.write = AsyncMock()

        project_id = await pm.create_project(
            name="Test Project",
            description="A test",
            agents=worker_specs,
            session_id="sess_001",
            initial_messages=[],
        )

        assert project_id.startswith("proj_")
        assert len(project_id) > 5


@pytest.mark.asyncio
async def test_create_project_sets_project_id_on_specs(
        mock_timeplus, mock_config, worker_specs):
    pm = make_project_manager(mock_timeplus, mock_config)

    with patch("pulsebot.agents.project_manager.ManagerAgent") as MockManager, \
         patch("pulsebot.agents.project_manager.SubAgent") as MockSubAgent, \
         patch("asyncio.create_task"):
        MockManager.return_value.run = AsyncMock()
        MockSubAgent.return_value.run = AsyncMock()
        pm._projects_writer.write = AsyncMock()
        pm._agents_writer.write = AsyncMock()

        project_id = await pm.create_project(
            name="Test Project",
            description="A test",
            agents=worker_specs,
            session_id="sess_001",
            initial_messages=[],
        )

        for spec in worker_specs:
            assert spec.project_id == project_id


@pytest.mark.asyncio
async def test_list_projects_empty_initially(mock_timeplus, mock_config):
    pm = make_project_manager(mock_timeplus, mock_config)
    projects = pm.list_projects()
    assert projects == []


@pytest.mark.asyncio
async def test_get_project_status_returns_none_for_unknown(
        mock_timeplus, mock_config):
    pm = make_project_manager(mock_timeplus, mock_config)
    status = pm.get_project_status("proj_nonexistent")
    assert status is None


@pytest.mark.asyncio
async def test_cancel_project_cancels_tasks(
        mock_timeplus, mock_config, worker_specs):
    pm = make_project_manager(mock_timeplus, mock_config)

    with patch("pulsebot.agents.project_manager.ManagerAgent") as MockManager, \
         patch("pulsebot.agents.project_manager.SubAgent") as MockSubAgent, \
         patch("asyncio.create_task") as mock_task:
        mock_task_handle = MagicMock()
        mock_task_handle.done = MagicMock(return_value=False)
        mock_task.return_value = mock_task_handle
        MockManager.return_value.run = AsyncMock()
        MockSubAgent.return_value.run = AsyncMock()
        pm._projects_writer.write = AsyncMock()
        pm._agents_writer.write = AsyncMock()

        project_id = await pm.create_project(
            name="Test", description="test",
            agents=worker_specs, session_id="sess_001",
            initial_messages=[],
        )

        result = await pm.cancel_project(project_id)
        assert result is True
        # Tasks should have been cancelled
        mock_task_handle.cancel.assert_called()


@pytest.mark.asyncio
async def test_create_project_raises_on_too_many_agents(
        mock_timeplus, mock_config):
    """Exceeding max_agents_per_project raises ValueError."""
    mock_config.multi_agent.max_agents_per_project = 2
    pm = make_project_manager(mock_timeplus, mock_config)

    specs = [
        SubAgentSpec(name=f"Agent{i}", task_description="task", project_id="", target_agents=[])
        for i in range(3)
    ]

    with pytest.raises(ValueError, match="Too many agents"):
        await pm.create_project(
            name="Big", description="big", agents=specs,
            session_id="s1", initial_messages=[],
        )


@pytest.mark.asyncio
async def test_create_project_raises_on_too_many_concurrent_projects(
        mock_timeplus, mock_config):
    """Exceeding max_concurrent_projects raises ValueError."""
    mock_config.multi_agent.max_concurrent_projects = 1
    pm = make_project_manager(mock_timeplus, mock_config)

    specs1 = [SubAgentSpec(name="A1", task_description="t", project_id="", target_agents=[])]
    specs2 = [SubAgentSpec(name="A2", task_description="t", project_id="", target_agents=[])]

    with patch("pulsebot.agents.project_manager.ManagerAgent"), \
         patch("pulsebot.agents.project_manager.SubAgent"), \
         patch("asyncio.create_task"):
        pm._projects_writer.write = AsyncMock()
        pm._agents_writer.write = AsyncMock()

        await pm.create_project(
            name="P1", description="first", agents=specs1,
            session_id="s1", initial_messages=[],
        )

        with pytest.raises(ValueError, match="Too many concurrent projects"):
            await pm.create_project(
                name="P2", description="second", agents=specs2,
                session_id="s2", initial_messages=[],
            )
