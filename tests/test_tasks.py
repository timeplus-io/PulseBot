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
        """Should CREATE FUNCTION and CREATE TASK via execute; metadata via insert."""
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

    def test_metadata_written_on_create(self, task_mgr, mock_client):
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
        assert record["task_type"] == "interval"
        assert record["schedule"] == "15m"

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

    def test_metadata_written_on_create(self, task_mgr, mock_client):
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
        assert record["task_type"] == "cron"
        assert record["schedule"] == "0 8 * * *"


class TestTaskLifecycle:
    def test_pause_issues_system_pause(self, task_mgr, mock_client):
        task_mgr.pause_task("user_weather_report")
        sqls = [c[0][0] for c in mock_client.execute.call_args_list]
        assert any("SYSTEM PAUSE TASK" in s for s in sqls)
        mock_client.insert.assert_not_called()

    def test_resume_issues_system_resume(self, task_mgr, mock_client):
        task_mgr.resume_task("user_weather_report")
        sqls = [c[0][0] for c in mock_client.execute.call_args_list]
        assert any("SYSTEM RESUME TASK" in s for s in sqls)
        mock_client.insert.assert_not_called()

    def test_drop_issues_drop_task(self, task_mgr, mock_client):
        task_mgr.drop_task("user_weather_report")
        sqls = [c[0][0] for c in mock_client.execute.call_args_list]
        assert any("DROP TASK" in s for s in sqls)
        mock_client.insert.assert_not_called()


class TestListTasks:
    def test_queries_proton_for_status(self, task_mgr, mock_client):
        mock_client.query.return_value = []
        task_mgr.list_tasks()
        first_query = mock_client.query.call_args_list[0][0][0]
        assert "SHOW TASKS" in first_query
        assert "verbose" in first_query

    def test_maps_status_0_to_active(self, task_mgr, mock_client):
        mock_client.query.side_effect = [
            [{"name": "user_foo", "status": 0}],
            [],  # schedules query
        ]
        result = task_mgr.list_tasks()
        assert result[0]["status"] == "active"

    def test_maps_status_1_to_paused(self, task_mgr, mock_client):
        mock_client.query.side_effect = [
            [{"name": "user_foo", "status": 1}],
            [],
        ]
        result = task_mgr.list_tasks()
        assert result[0]["status"] == "paused"

    def test_schedule_merged_from_metadata(self, task_mgr, mock_client):
        mock_client.query.side_effect = [
            [{"name": "user_foo", "status": 0}],
            [{"name": "user_foo", "schedule": "1h"}],
        ]
        result = task_mgr.list_tasks()
        assert result[0]["schedule"] == "1h"

    def test_missing_schedule_defaults_to_empty(self, task_mgr, mock_client):
        mock_client.query.side_effect = [
            [{"name": "user_foo", "status": 0}],
            [],
        ]
        result = task_mgr.list_tasks()
        assert result[0]["schedule"] == ""

    def test_schedule_query_failure_does_not_break_list(self, task_mgr, mock_client):
        mock_client.query.side_effect = [
            [{"name": "user_foo", "status": 0}],
            Exception("stream unavailable"),
        ]
        result = task_mgr.list_tasks()
        assert len(result) == 1
        assert result[0]["status"] == "active"
