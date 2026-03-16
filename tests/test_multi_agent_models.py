"""Tests for multi-agent data models."""

from pulsebot.agents.models import ProjectState, SubAgentSpec


def test_subagentspec_default_agent_id_derived_from_name():
    spec = SubAgentSpec(
        name="SQL Analyst",
        task_description="Analyze data",
        project_id="proj_001",
        target_agents=[],
    )
    assert spec.agent_id == "agent_sql_analyst"


def test_subagentspec_explicit_agent_id_overrides_derivation():
    spec = SubAgentSpec(
        name="Analyst",
        agent_id="my_custom_id",
        task_description="Analyze data",
        project_id="proj_001",
        target_agents=[],
    )
    assert spec.agent_id == "my_custom_id"


def test_subagentspec_defaults():
    spec = SubAgentSpec(
        name="Researcher",
        task_description="Research things",
        project_id="proj_001",
        target_agents=["agent_analyst"],
    )
    assert spec.role == "worker"
    assert spec.model is None
    assert spec.provider is None
    assert spec.temperature is None
    assert spec.max_iterations == 5
    assert spec.enable_memory is False
    assert spec.skills is None
    assert spec.skill_overrides is None
    assert spec.timeout_seconds == 300
    assert spec.checkpoint_sn == 0


def test_subagentspec_with_skill_overrides():
    spec = SubAgentSpec(
        name="Shell Worker",
        task_description="Run commands",
        project_id="proj_001",
        target_agents=[],
        skills=["shell"],
        skill_overrides={"shell": {"allowed_commands": ["grep"]}},
    )
    assert spec.skills == ["shell"]
    assert spec.skill_overrides["shell"]["allowed_commands"] == ["grep"]


def test_subagentspec_hyphenated_name_derives_agent_id():
    spec = SubAgentSpec(
        name="Report-Writer",
        task_description="Write reports",
        project_id="proj_001",
        target_agents=[],
    )
    assert spec.agent_id == "agent_report_writer"


def test_projectstate_fields():
    state = ProjectState(
        project_id="proj_abc",
        name="Test Project",
        description="A test",
        session_id="sess_123",
        agent_ids=["agent_a", "agent_b"],
    )
    assert state.status == "active"
    assert state.project_id == "proj_abc"
    assert "agent_a" in state.agent_ids
