# tests/test_notifier.py
"""Tests for NotificationDispatcher."""
from __future__ import annotations
from unittest.mock import AsyncMock
import json
import pytest
from pulsebot.core.notifier import NotificationDispatcher


@pytest.fixture
def mock_events_writer():
    writer = AsyncMock()
    writer.write = AsyncMock(return_value="event-id-1")
    return writer


@pytest.fixture
def dispatcher(mock_events_writer):
    return NotificationDispatcher(mock_events_writer)


class TestNotificationDispatcher:
    @pytest.mark.asyncio
    async def test_broadcast_writes_to_events_stream(self, dispatcher, mock_events_writer):
        await dispatcher.broadcast_task_result(
            task_name="weather_report",
            text="Current weather: sunny",
            session_id="global_task_weather_report",
        )
        mock_events_writer.write.assert_called_once()

    @pytest.mark.asyncio
    async def test_event_type_is_task_notification(self, dispatcher, mock_events_writer):
        await dispatcher.broadcast_task_result(
            task_name="weather_report",
            text="sunny",
            session_id="global_task_weather_report",
        )
        call_data = mock_events_writer.write.call_args[0][0]
        assert call_data["event_type"] == "task_notification"

    @pytest.mark.asyncio
    async def test_payload_contains_task_name_and_text(self, dispatcher, mock_events_writer):
        await dispatcher.broadcast_task_result(
            task_name="morning_brief",
            text="Market is up 2%",
            session_id="global_task_morning_brief",
        )
        call_data = mock_events_writer.write.call_args[0][0]
        payload = json.loads(call_data["payload"])
        assert payload["task_name"] == "morning_brief"
        assert payload["text"] == "Market is up 2%"
        assert payload["session_id"] == "global_task_morning_brief"

    @pytest.mark.asyncio
    async def test_broadcast_handles_writer_failure_gracefully(self, dispatcher, mock_events_writer):
        mock_events_writer.write.side_effect = Exception("stream down")
        # Should not raise; logs warning instead
        await dispatcher.broadcast_task_result("t", "msg", "s")
