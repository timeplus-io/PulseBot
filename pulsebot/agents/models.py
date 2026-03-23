"""Data models for the multi-agent system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _derive_agent_id(name: str) -> str:
    """Derive a stable agent ID from a human-readable name.

    'SQL Analyst' -> 'agent_sql_analyst'
    'Report Writer' -> 'agent_report_writer'
    """
    slug = name.lower().replace(" ", "_").replace("-", "_")
    return f"agent_{slug}"


@dataclass
class SubAgentSpec:
    """Specification for creating a sub-agent."""

    # Identity
    name: str
    task_description: str
    project_id: str
    target_agents: list[str]

    # Auto-derived from name if not provided
    agent_id: str = ""
    role: str = "worker"  # "manager" or "worker"

    # LLM overrides (None = inherit from main agent config)
    model: str | None = None
    provider: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    max_iterations: int = 5
    enable_memory: bool = False

    # Skill configuration (None = inherit all from main agent)
    skills: list[str] | None = None
    skill_overrides: dict[str, Any] | None = None

    # Builtin skills always included regardless of `skills` filter.
    # None = use the default set (file_ops, shell, workspace).
    builtin_skills: list[str] | None = None

    # Execution
    timeout_seconds: int = 300
    checkpoint_sn: int = 0

    def __post_init__(self) -> None:
        if not self.agent_id:
            self.agent_id = _derive_agent_id(self.name)


@dataclass
class ProjectState:
    """Runtime state of a multi-agent project."""

    project_id: str
    name: str
    description: str
    session_id: str
    agent_ids: list[str]
    status: str = "active"  # 'active', 'completed', 'failed', 'cancelled'
    config_overrides: dict[str, Any] = field(default_factory=dict)
    created_by: str = ""   # agent or user that originated the project
