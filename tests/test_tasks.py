"""Tests for TaskManager UDF-based task creation."""
from __future__ import annotations
from unittest.mock import MagicMock, call
import pytest
from pulsebot.timeplus.tasks import TaskManager


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.execute = MagicMock()
    client.insert = MagicMock()
    client.query = MagicMock(return_value=[])
    return client


@pytest.fixture
def task_mgr(mock_client):
    return TaskManager(mock_client)


class TestCreateIntervalTask:
    def test_issues_two_sql_calls(self, task_mgr, mock_client):
        """Should CREATE FUNCTION and CREATE TASK via execute; status via insert."""
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

    def test_status_written_as_active(self, task_mgr, mock_client):
        task_mgr.create_interval_task(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )
        mock_client.insert.assert_called_once()
        insert_args = mock_client.insert.call_args
        assert insert_args[0][0] == "pulsebot.tasks"
        record = insert_args[0][1][0]
        assert record["status"] == "active"
        assert record["task_type"] == "interval"

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
        assert "http://localhost:8000" in udf_sql

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

    def test_status_written_as_active(self, task_mgr, mock_client):
        task_mgr.create_cron_task(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )
        mock_client.insert.assert_called_once()
        insert_args = mock_client.insert.call_args
        assert insert_args[0][0] == "pulsebot.tasks"
        record = insert_args[0][1][0]
        assert record["status"] == "active"
        assert record["task_type"] == "cron"


class TestStatusTracking:
    def test_pause_writes_paused_status(self, task_mgr, mock_client):
        task_mgr.pause_task("user_weather_report")
        sqls = [c[0][0] for c in mock_client.execute.call_args_list]
        assert any("SYSTEM PAUSE TASK" in s for s in sqls)
        insert_args = mock_client.insert.call_args
        record = insert_args[0][1][0]
        assert record["status"] == "paused"

    def test_resume_writes_active_status(self, task_mgr, mock_client):
        task_mgr.resume_task("user_weather_report")
        sqls = [c[0][0] for c in mock_client.execute.call_args_list]
        assert any("SYSTEM RESUME TASK" in s for s in sqls)
        insert_args = mock_client.insert.call_args
        record = insert_args[0][1][0]
        assert record["status"] == "active"

    def test_drop_writes_deleted_status(self, task_mgr, mock_client):
        task_mgr.drop_task("user_weather_report")
        sqls = [c[0][0] for c in mock_client.execute.call_args_list]
        assert any("DROP TASK" in s for s in sqls)
        insert_args = mock_client.insert.call_args
        record = insert_args[0][1][0]
        assert record["status"] == "deleted"

    def test_list_queries_tasks_stream(self, task_mgr, mock_client):
        task_mgr.list_tasks()
        mock_client.query.assert_called_once()
        query = mock_client.query.call_args[0][0]
        assert "pulsebot.tasks" in query
        assert "arg_max" in query
        assert "status != 'deleted'" in query

    def test_list_falls_back_to_show_tasks_on_error(self, task_mgr, mock_client):
        mock_client.query.side_effect = [Exception("stream unavailable"), []]
        result = task_mgr.list_tasks()
        assert mock_client.query.call_count == 2
        fallback_query = mock_client.query.call_args_list[1][0][0]
        assert "SHOW TASKS" in fallback_query
