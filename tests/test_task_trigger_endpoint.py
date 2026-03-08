# tests/test_task_trigger_endpoint.py
"""Tests for POST /api/v1/task-trigger endpoint."""
from __future__ import annotations
from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def app():
    from pulsebot.api.server import create_app
    with patch("pulsebot.api.server.lifespan"):
        application = create_app()
    return application


@pytest.fixture
def mock_writer():
    writer = AsyncMock()
    writer.write = AsyncMock(return_value="exec-id-123")
    return writer


class TestTaskTriggerEndpoint:
    @pytest.fixture(autouse=True)
    def patch_writer(self, mock_writer, monkeypatch):
        import pulsebot.api.server as srv
        monkeypatch.setattr(srv, "_writer", mock_writer)

    def test_valid_interval_trigger(self, app, mock_writer):
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.post("/api/v1/task-trigger", json={
            "task_id": "task-abc",
            "task_name": "weather_report",
            "prompt": "Get current weather",
            "trigger_type": "interval",
        })

        assert resp.status_code == 200
        body = resp.json()
        assert body["execution_id"]
        assert body["session_id"] == "global_task_weather_report"

    def test_missing_prompt_returns_422(self, app, mock_writer):
        client = TestClient(app)

        resp = client.post("/api/v1/task-trigger", json={
            "task_id": "task-abc",
            "task_name": "weather_report",
            # prompt missing
            "trigger_type": "interval",
        })
        assert resp.status_code == 422

    def test_message_written_with_correct_fields(self, app, mock_writer):
        client = TestClient(app)

        client.post("/api/v1/task-trigger", json={
            "task_id": "task-abc",
            "task_name": "my_task",
            "prompt": "Do something",
            "trigger_type": "interval",
        })

        call_args = mock_writer.write.call_args[0][0]
        assert call_args["session_id"] == "global_task_my_task"
        assert call_args["message_type"] == "scheduled_task"
        assert call_args["target"] == "agent"
        assert "Do something" in call_args["content"]

    def test_returns_500_when_not_initialized(self, app, monkeypatch):
        import pulsebot.api.server as srv
        monkeypatch.setattr(srv, "_writer", None)
        client = TestClient(app, raise_server_exceptions=False)
        resp = client.post("/api/v1/task-trigger", json={
            "task_id": "t1", "task_name": "n", "prompt": "p"
        })
        assert resp.status_code == 500
