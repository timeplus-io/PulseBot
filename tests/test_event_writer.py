# tests/test_event_writer.py
from __future__ import annotations
import json
from unittest.mock import AsyncMock, MagicMock
import pytest
from pulsebot.timeplus.event_writer import EventWriter


def _make_writer():
    mock_writer = MagicMock()
    mock_writer.write = AsyncMock()
    return mock_writer, EventWriter(mock_writer, default_source="agent:test", default_tags=["agent:test"])


@pytest.mark.asyncio
async def test_emit_writes_to_stream():
    mock_writer, ew = _make_writer()
    await ew.emit("agent.ready", payload={"agent_id": "main"})
    mock_writer.write.assert_called_once()
    call_data = mock_writer.write.call_args[0][0]
    assert call_data["event_type"] == "agent.ready"
    assert call_data["source"] == "agent:test"
    assert call_data["severity"] == "info"
    assert "lifecycle" in call_data["tags"]
    payload = json.loads(call_data["payload"])
    assert payload["agent_id"] == "main"


@pytest.mark.asyncio
async def test_emit_severity_filtering():
    mock_writer = MagicMock()
    mock_writer.write = AsyncMock()
    ew = EventWriter(mock_writer, default_source="test", min_severity="warning")
    await ew.emit("agent.state.thinking", severity="debug", payload={})
    await ew.emit("agent.state.thinking", severity="info", payload={})
    mock_writer.write.assert_not_called()
    await ew.emit("agent.error", severity="error", payload={})
    mock_writer.write.assert_called_once()


@pytest.mark.asyncio
async def test_emit_tag_merging():
    mock_writer, ew = _make_writer()
    await ew.emit("tool.call_completed", tags=["security"])
    call_data = mock_writer.write.call_args[0][0]
    assert "agent:test" in call_data["tags"]
    assert "security" in call_data["tags"]
    assert "tool" in call_data["tags"]


@pytest.mark.asyncio
async def test_emit_error_captures_traceback():
    mock_writer, ew = _make_writer()
    try:
        raise ValueError("test error")
    except ValueError as e:
        await ew.emit_error("agent.crash", e, payload={"agent_id": "main"})
    call_data = mock_writer.write.call_args[0][0]
    assert call_data["severity"] == "error"
    payload = json.loads(call_data["payload"])
    assert payload["error"] == "test error"
    assert payload["error_type"] == "ValueError"
    assert "traceback" in payload


@pytest.mark.asyncio
async def test_emit_source_override():
    mock_writer, ew = _make_writer()
    await ew.emit("agent.ready", source="custom:source")
    call_data = mock_writer.write.call_args[0][0]
    assert call_data["source"] == "custom:source"


@pytest.mark.asyncio
async def test_emit_unknown_category_uses_general():
    mock_writer, ew = _make_writer()
    await ew.emit("unknown.event_type")
    call_data = mock_writer.write.call_args[0][0]
    assert "general" in call_data["tags"]


@pytest.mark.asyncio
async def test_emit_noop_when_writer_none():
    ew = EventWriter(None, default_source="test")  # type: ignore[arg-type]
    await ew.emit("agent.ready")  # must not raise


@pytest.mark.asyncio
async def test_emit_swallows_write_errors():
    failing_writer = MagicMock()
    failing_writer.write = AsyncMock(side_effect=RuntimeError("DB unavailable"))
    ew = EventWriter(failing_writer, default_source="test")
    await ew.emit("agent.ready", payload={"agent_id": "main"})  # must not raise


@pytest.mark.asyncio
async def test_emit_severity_levels_count():
    mock_writer = MagicMock()
    mock_writer.write = AsyncMock()
    ew = EventWriter(mock_writer, default_source="test", min_severity="info")
    await ew.emit("x.a", severity="debug")
    await ew.emit("x.b", severity="info")
    await ew.emit("x.c", severity="warning")
    await ew.emit("x.d", severity="error")
    await ew.emit("x.e", severity="critical")
    assert mock_writer.write.call_count == 4
