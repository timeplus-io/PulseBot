"""Tests for Telegram channel handling task_notification events."""
from __future__ import annotations
from unittest.mock import AsyncMock, MagicMock, patch
import json
import pytest


@pytest.fixture
def channel():
    from pulsebot.channels.telegram import TelegramChannel
    with patch("pulsebot.channels.telegram.Application"):
        ch = TelegramChannel.__new__(TelegramChannel)
        # _sessions is dict[int, str]: chat_id -> session_id
        ch._sessions = {
            111: "tg_111_aaa",
            222: "tg_222_bbb",
        }
        # Mock _app.bot.send_message
        mock_bot = AsyncMock()
        mock_bot.send_message = AsyncMock()
        mock_app = MagicMock()
        mock_app.bot = mock_bot
        ch._app = mock_app
        return ch


class TestTelegramTaskBroadcast:
    @pytest.mark.asyncio
    async def test_broadcast_event_sends_to_all_chats(self, channel):
        payload = json.dumps({
            "task_name": "weather_report",
            "text": "Sunny today!",
            "session_id": "global_task_weather_report",
        })
        await channel._handle_task_notification(payload)

        assert channel._app.bot.send_message.call_count == 2
        chat_ids = {c.kwargs["chat_id"]
                    for c in channel._app.bot.send_message.call_args_list}
        assert chat_ids == {111, 222}

    @pytest.mark.asyncio
    async def test_broadcast_sends_correct_text(self, channel):
        payload = json.dumps({
            "task_name": "weather_report",
            "text": "Sunny today!",
            "session_id": "global_task_weather_report",
        })
        await channel._handle_task_notification(payload)

        sent_text = channel._app.bot.send_message.call_args_list[0].kwargs["text"]
        assert "Sunny today!" in sent_text

    @pytest.mark.asyncio
    async def test_no_active_chats_does_not_raise(self, channel):
        channel._sessions = {}
        await channel._handle_task_notification(
            json.dumps({"task_name": "t", "text": "msg", "session_id": "s"})
        )
        channel._app.bot.send_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_invalid_json_does_not_raise(self, channel):
        await channel._handle_task_notification("not-json")
        channel._app.bot.send_message.assert_not_called()
