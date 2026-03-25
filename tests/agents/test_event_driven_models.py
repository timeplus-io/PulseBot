from pulsebot.agents.models import ProjectState, SubAgentSpec


def test_sub_agent_spec_has_event_fields():
    spec = SubAgentSpec(
        name="Test",
        task_description="desc",
        project_id="proj_1",
        target_agents=[],
    )
    assert spec.event_query == ""
    assert spec.context_field == ""

def test_sub_agent_spec_event_fields_set():
    spec = SubAgentSpec(
        name="Test",
        task_description="desc",
        project_id="proj_1",
        target_agents=[],
        event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        context_field="payload",
    )
    assert spec.event_query == "SELECT payload FROM pulsebot.events WHERE severity = 'error'"
    assert spec.context_field == "payload"

def test_project_state_has_event_fields():
    state = ProjectState(
        project_id="proj_1",
        name="Test",
        description="desc",
        session_id="sess_1",
        agent_ids=["agent_a"],
    )
    assert state.event_query == ""
    assert state.context_field == ""


def test_project_state_event_fields_set():
    state = ProjectState(
        project_id="proj_1",
        name="Test",
        description="desc",
        session_id="sess_1",
        agent_ids=["agent_a"],
        event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        context_field="payload",
    )
    assert state.event_query == "SELECT payload FROM pulsebot.events WHERE severity = 'error'"
    assert state.context_field == "payload"
