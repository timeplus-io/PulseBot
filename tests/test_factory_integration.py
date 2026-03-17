# tests/test_factory_integration.py
"""Tests for factory.py project_manager skill integration."""

from unittest.mock import MagicMock, patch

from pulsebot.config import Config, MultiAgentConfig


def test_create_skill_loader_registers_project_manager_when_configured():
    """When 'project_manager' is in skills.builtin, it should be registered."""
    config = Config()
    config.skills.builtin = ["project_manager"]
    config.multi_agent = MultiAgentConfig()

    mock_timeplus = MagicMock()
    mock_timeplus.host = "localhost"
    mock_timeplus.port = 8463
    mock_timeplus.username = "default"
    mock_timeplus.password = ""

    mock_llm = MagicMock()
    mock_executor = MagicMock()

    with patch("pulsebot.timeplus.client.TimeplusClient") as MockClient, \
         patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter"), \
         patch("pulsebot.agents.project_manager.StreamWriter"):
        MockClient.return_value = mock_timeplus
        MockClient.from_config.return_value = mock_timeplus

        from pulsebot.factory import create_skill_loader
        loader = create_skill_loader(
            config,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            executor=mock_executor,
        )

    skill = loader.get_skill("project_manager")
    assert skill is not None
    assert skill.name == "project_manager"
    tool_names = {t.name for t in skill.get_tools()}
    assert "create_project" in tool_names


def test_create_skill_loader_without_project_manager():
    """Without project_manager in builtin list, skill should not be loaded."""
    config = Config()
    config.skills.builtin = ["file_ops"]

    from pulsebot.factory import create_skill_loader
    loader = create_skill_loader(config)

    skill = loader.get_skill("project_manager")
    assert skill is None
