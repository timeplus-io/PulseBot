"""Integration tests: verify events are emitted at key lifecycle points."""
from __future__ import annotations
import json
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from pulsebot.core.agent import Agent
from pulsebot.timeplus.event_writer import EventWriter


def _make_agent(min_event_severity="debug"):
    """Build a minimal Agent with mocked dependencies."""
    tp = MagicMock()
    tp.host = "localhost"
    tp.port = 8463
    tp.username = "default"
    tp.password = ""

    llm = MagicMock()
    llm.model = "test-model"
    llm.provider_name = "test"
    llm.get_tool_definitions = MagicMock(return_value=[])

    skills = MagicMock()
    skills.get_tools = MagicMock(return_value=[])
    skills.format_skills_for_prompt = MagicMock(return_value="")
    skills._skill_dirs = []
    skills.set_events = AsyncMock()

    # TimeplusClient is imported inside Agent.__init__ so we patch it at its
    # definition site (pulsebot.timeplus.client) and also at the local import
    # path used inside the method.
    with patch("pulsebot.timeplus.client.TimeplusClient"):
        with patch("pulsebot.core.agent.TimeplusClient", create=True):
            agent = Agent(
                agent_id="test",
                timeplus=tp,
                llm_provider=llm,
                skill_loader=skills,
                min_event_severity=min_event_severity,
            )
    return agent


@pytest.mark.asyncio
async def test_agent_has_events_writer():
    agent = _make_agent()
    assert hasattr(agent, "events")
    assert isinstance(agent.events, EventWriter)


@pytest.mark.asyncio
async def test_agent_emits_agent_ready_and_stopped():
    agent = _make_agent()
    # Replace event writer's internal stream writer with a mock
    mock_sw = MagicMock()
    mock_sw.write = AsyncMock()
    agent.events._writer = mock_sw

    with patch.object(agent, "_ensure_streams_exist", AsyncMock()):
        with patch.object(agent.messages_reader, "stream") as mock_stream:
            # empty_stream is an async generator that yields nothing.
            # The unreachable `yield` is required so Python treats the
            # function as an async generator (not a coroutine).
            async def empty_stream(_):
                return
                yield  # noqa: unreachable — required to make this an async generator

            mock_stream.return_value = empty_stream(None)
            await agent.run()

    calls = [c[0][0] for c in mock_sw.write.call_args_list]
    event_types = [c["event_type"] for c in calls]
    assert "agent.ready" in event_types
    assert "agent.stopped" in event_types


@pytest.mark.asyncio
async def test_executor_emits_tool_events():
    from pulsebot.core.executor import ToolExecutor

    mock_sw = MagicMock()
    mock_sw.write = AsyncMock()
    events = EventWriter(mock_sw, default_source="test")

    skills = MagicMock()
    skill = MagicMock()
    skill.execute = AsyncMock(return_value=MagicMock(success=True, output="ok", error=None))
    skills.get_skill_for_tool = MagicMock(return_value=skill)
    skills.get_tool_definitions = MagicMock(return_value=[])

    executor = ToolExecutor(skills, events=events)
    await executor.execute("test_tool", {"arg": "val"}, session_id="sess1")

    calls = [c[0][0] for c in mock_sw.write.call_args_list]
    event_types = [c["event_type"] for c in calls]
    assert "tool.call_started" in event_types
    assert "tool.call_completed" in event_types


@pytest.mark.asyncio
async def test_executor_emits_hook_denied_event():
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.hooks.base import HookVerdict, ToolCallHook

    mock_sw = MagicMock()
    mock_sw.write = AsyncMock()
    events = EventWriter(mock_sw, default_source="test")

    class DenyHook(ToolCallHook):
        async def pre_call(self, tool_name, arguments, session_id=""):
            return HookVerdict(verdict="deny", reasoning="blocked")
        async def post_call(self, tool_name, arguments, result, session_id=""):
            pass

    skills = MagicMock()
    skills.get_tool_definitions = MagicMock(return_value=[])
    executor = ToolExecutor(skills, hooks=[DenyHook()], events=events)
    await executor.execute("shell", {}, session_id="sess1")

    calls = [c[0][0] for c in mock_sw.write.call_args_list]
    event_types = [c["event_type"] for c in calls]
    assert "tool.hook_denied" in event_types
