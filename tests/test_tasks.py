"""Tests for TaskManager UDF-based task creation."""
from __future__ import annotations
from unittest.mock import MagicMock
import pytest
from pulsebot.timeplus.tasks import TaskManager


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.execute = MagicMock()
    client.query = MagicMock(return_value=[])
    return client


@pytest.fixture
def task_mgr(mock_client):
    return TaskManager(mock_client)


class TestCreateIntervalTask:
    def test_issues_two_sql_calls(self, task_mgr, mock_client):
        """Should CREATE FUNCTION then CREATE TASK."""
        task_mgr.create_interval_task(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )
        assert mock_client.execute.call_count == 2

    def test_udf_sql_contains_api_url(self, task_mgr, mock_client):
        task_mgr.create_interval_task(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )
        udf_sql = mock_client.execute.call_args_list[0][0][0]
        assert "http://localhost:8000" in udf_sql
        assert "trigger_pulsebot_task" in udf_sql

    def test_task_sql_contains_schedule_and_prompt(self, task_mgr, mock_client):
        task_mgr.create_interval_task(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        assert "15m" in task_sql
        assert "weather_report" in task_sql   # sanitised name
        assert "Get the weather" in task_sql
        assert "trigger_pulsebot_task" in task_sql

    def test_name_sanitised(self, task_mgr, mock_client):
        task_mgr.create_interval_task(
            name="My Task! #1",
            prompt="do stuff",
            interval="1h",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        assert "user_my_task_1" in task_sql

    def test_returns_sanitised_name(self, task_mgr, mock_client):
        result = task_mgr.create_interval_task(
            name="daily-report",
            prompt="...",
            interval="1h",
            api_url="http://localhost:8000",
        )
        assert result == "user_daily_report"


class TestCreateCronTask:
    def test_issues_two_sql_calls(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        assert mock_client.execute.call_count == 2

    def test_udf_contains_cron_matching(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        udf_sql = mock_client.execute.call_args_list[0][0][0]
        assert "check_cron_and_trigger" in udf_sql
        assert "matches_cron" in udf_sql
        assert "http://localhost:8000" in udf_sql  # ← add this line

    def test_task_uses_1m_schedule(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        # Cron tasks poll every 1 minute, matching inside the UDF
        assert "1m" in task_sql

    def test_cron_expression_embedded_in_task(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        task_sql = mock_client.execute.call_args_list[1][0][0]
        assert "0 8 * * *" in task_sql
