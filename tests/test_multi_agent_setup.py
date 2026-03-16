"""Tests for multi-agent stream DDL and config."""

from pulsebot.config import Config, MultiAgentConfig
from pulsebot.timeplus.setup import (
    KANBAN_AGENTS_STREAM_DDL,
    KANBAN_PROJECTS_STREAM_DDL,
    KANBAN_STREAM_DDL,
)


def test_kanban_ddl_has_required_fields():
    assert "msg_id" in KANBAN_STREAM_DDL
    assert "project_id" in KANBAN_STREAM_DDL
    assert "sender_id" in KANBAN_STREAM_DDL
    assert "target_id" in KANBAN_STREAM_DDL
    assert "msg_type" in KANBAN_STREAM_DDL
    assert "content" in KANBAN_STREAM_DDL


def test_kanban_projects_ddl_has_required_fields():
    assert "project_id" in KANBAN_PROJECTS_STREAM_DDL
    assert "status" in KANBAN_PROJECTS_STREAM_DDL
    assert "session_id" in KANBAN_PROJECTS_STREAM_DDL
    assert "agent_ids" in KANBAN_PROJECTS_STREAM_DDL


def test_kanban_agents_ddl_has_required_fields():
    assert "agent_id" in KANBAN_AGENTS_STREAM_DDL
    assert "project_id" in KANBAN_AGENTS_STREAM_DDL
    assert "role" in KANBAN_AGENTS_STREAM_DDL
    assert "checkpoint_sn" in KANBAN_AGENTS_STREAM_DDL
    assert "skills" in KANBAN_AGENTS_STREAM_DDL


def test_multi_agent_config_defaults():
    cfg = MultiAgentConfig()
    assert cfg.enabled is True
    assert cfg.max_agents_per_project == 10
    assert cfg.max_concurrent_projects == 5
    assert cfg.default_agent_timeout == 300
    assert cfg.project_timeout == 1800
    assert cfg.checkpoint_interval == 1


def test_config_includes_multi_agent():
    cfg = Config()
    assert hasattr(cfg, "multi_agent")
    assert isinstance(cfg.multi_agent, MultiAgentConfig)
