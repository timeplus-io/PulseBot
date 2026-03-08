# tests/test_scheduler_skill.py
"""Tests for SchedulerSkill."""
from __future__ import annotations
from unittest.mock import MagicMock, AsyncMock
import pytest
from pulsebot.skills.builtin.scheduler import SchedulerSkill, _convert_cron_to_utc


@pytest.fixture
def mock_task_mgr():
    mgr = MagicMock()
    mgr.create_interval_task = MagicMock(return_value="user_weather_report")
    mgr.create_cron_task = MagicMock(return_value="user_morning_brief")
    mgr.list_tasks = MagicMock(return_value=[
        {"name": "user_weather_report", "status": "Running"},
        {"name": "heartbeat_task", "status": "Running"},  # system — filtered out
    ])
    mgr.drop_task = MagicMock()
    mgr.pause_task = MagicMock()
    mgr.resume_task = MagicMock()
    return mgr


@pytest.fixture
def skill(mock_task_mgr):
    s = SchedulerSkill.__new__(SchedulerSkill)
    s.task_manager = mock_task_mgr
    s.api_url = "http://localhost:8000"
    return s


class TestSchedulerSkillTools:
    def test_exposes_six_tools(self, skill):
        names = {t.name for t in skill.get_tools()}
        assert names == {
            "create_interval_task",
            "create_cron_task",
            "list_tasks",
            "pause_task",
            "resume_task",
            "delete_task",
        }


class TestCreateIntervalTask:
    @pytest.mark.asyncio
    async def test_success(self, skill, mock_task_mgr):
        result = await skill.execute("create_interval_task", {
            "name": "weather-report",
            "prompt": "Get the weather",
            "interval": "15m",
        })
        assert result.success
        mock_task_mgr.create_interval_task.assert_called_once_with(
            name="weather-report",
            prompt="Get the weather",
            interval="15m",
            api_url="http://localhost:8000",
        )

    @pytest.mark.asyncio
    async def test_failure_returns_error(self, skill, mock_task_mgr):
        mock_task_mgr.create_interval_task.side_effect = Exception("DB error")
        result = await skill.execute("create_interval_task",
                                     {"name": "x", "prompt": "y", "interval": "1h"})
        assert not result.success
        assert "DB error" in result.error


class TestCreateCronTask:
    @pytest.mark.asyncio
    async def test_success(self, skill, mock_task_mgr):
        result = await skill.execute("create_cron_task", {
            "name": "morning-brief",
            "prompt": "Daily briefing",
            "cron": "0 8 * * *",
        })
        assert result.success
        mock_task_mgr.create_cron_task.assert_called_once_with(
            name="morning-brief",
            prompt="Daily briefing",
            cron="0 8 * * *",
            api_url="http://localhost:8000",
        )

    @pytest.mark.asyncio
    async def test_failure_returns_error(self, skill, mock_task_mgr):
        mock_task_mgr.create_cron_task.side_effect = Exception("DB error")
        result = await skill.execute("create_cron_task",
                                     {"name": "x", "prompt": "y", "cron": "0 8 * * *"})
        assert not result.success
        assert "DB error" in result.error


class TestListTasks:
    @pytest.mark.asyncio
    async def test_only_user_tasks_shown(self, skill):
        result = await skill.execute("list_tasks", {})
        assert result.success
        assert "user_weather_report" in result.output
        assert "heartbeat_task" not in result.output   # system task filtered

    @pytest.mark.asyncio
    async def test_empty_list_message(self, skill, mock_task_mgr):
        mock_task_mgr.list_tasks.return_value = []
        result = await skill.execute("list_tasks", {})
        assert result.success
        assert "no" in result.output.lower()


class TestPauseResumeDelete:
    @pytest.mark.asyncio
    async def test_pause_user_task(self, skill, mock_task_mgr):
        result = await skill.execute("pause_task", {"name": "user_weather_report"})
        assert result.success
        mock_task_mgr.pause_task.assert_called_once_with("user_weather_report")

    @pytest.mark.asyncio
    async def test_resume_user_task(self, skill, mock_task_mgr):
        result = await skill.execute("resume_task", {"name": "user_weather_report"})
        assert result.success
        mock_task_mgr.resume_task.assert_called_once_with("user_weather_report")

    @pytest.mark.asyncio
    async def test_delete_user_task(self, skill, mock_task_mgr):
        result = await skill.execute("delete_task", {"name": "user_weather_report"})
        assert result.success
        mock_task_mgr.drop_task.assert_called_once_with("user_weather_report")

    @pytest.mark.asyncio
    async def test_cannot_delete_system_task(self, skill, mock_task_mgr):
        result = await skill.execute("delete_task", {"name": "heartbeat_task"})
        assert not result.success
        mock_task_mgr.drop_task.assert_not_called()

    @pytest.mark.asyncio
    async def test_cannot_pause_system_task(self, skill, mock_task_mgr):
        result = await skill.execute("pause_task", {"name": "daily_summary"})
        assert not result.success

    @pytest.mark.asyncio
    async def test_cannot_resume_system_task(self, skill, mock_task_mgr):
        result = await skill.execute("resume_task", {"name": "daily_summary"})
        assert not result.success
        mock_task_mgr.resume_task.assert_not_called()


class TestConvertCronToUtc:
    def test_utc_passthrough(self):
        assert _convert_cron_to_utc("0 8 * * *", "UTC") == "0 8 * * *"

    def test_positive_offset(self):
        # Asia/Shanghai is UTC+8: 11:00 CST → 03:00 UTC same day
        result = _convert_cron_to_utc("0 11 * * *", "Asia/Shanghai")
        assert result == "0 3 * * *"

    def test_negative_offset_same_day(self):
        # America/Phoenix is UTC-7 year-round (no DST): 11:00 → 18:00 UTC
        result = _convert_cron_to_utc("0 11 * * *", "America/Phoenix")
        minute, hour, *_ = result.split()
        assert hour == "18"

    def test_midnight_crossing_shifts_dow(self):
        # UTC+8: 23:00 Friday (dow=5) → 15:00 UTC Friday (no shift needed)
        # UTC-8 (US/Pacific): 23:00 Friday → 07:00 UTC Saturday (dow 5→6)
        result = _convert_cron_to_utc("0 23 * * 5", "US/Pacific")
        parts = result.split()
        assert parts[4] == "6"   # Saturday in UTC

    def test_dow_wraps_saturday_to_sunday(self):
        # UTC-8: 23:00 Saturday (dow=6) → 07:00 UTC Sunday (dow 6→0)
        result = _convert_cron_to_utc("0 23 * * 6", "US/Pacific")
        parts = result.split()
        assert parts[4] == "0"

    def test_wildcard_hours_unchanged(self):
        # Can't convert a wildcard hour
        assert _convert_cron_to_utc("* * * * *", "America/New_York") == "* * * * *"

    def test_unknown_timezone_raises(self):
        with pytest.raises(ValueError, match="Unknown timezone"):
            _convert_cron_to_utc("0 8 * * *", "Invalid/Zone")

    def test_wrong_field_count_raises(self):
        with pytest.raises(ValueError, match="5-field"):
            _convert_cron_to_utc("0 8 * *", "UTC")

    @pytest.mark.asyncio
    async def test_create_cron_task_with_timezone(self, skill, mock_task_mgr):
        result = await skill.execute("create_cron_task", {
            "name": "morning-brief",
            "prompt": "Daily briefing",
            "cron": "0 11 * * *",
            "timezone": "Asia/Shanghai",
        })
        assert result.success
        # Should pass UTC-converted cron (03:00 UTC) to task manager
        call_args = mock_task_mgr.create_cron_task.call_args
        assert call_args.kwargs["cron"] == "0 3 * * *"
        assert "Asia/Shanghai" in result.output

    @pytest.mark.asyncio
    async def test_create_cron_task_default_utc(self, skill, mock_task_mgr):
        result = await skill.execute("create_cron_task", {
            "name": "morning-brief",
            "prompt": "Daily briefing",
            "cron": "0 8 * * *",
        })
        assert result.success
        call_args = mock_task_mgr.create_cron_task.call_args
        assert call_args.kwargs["cron"] == "0 8 * * *"
