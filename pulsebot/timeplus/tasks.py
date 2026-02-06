"""Timeplus task management for PulseBot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class TaskManager:
    """Manage Timeplus Tasks (SQL-native scheduling).
    
    Timeplus Tasks replace traditional cron jobs with streaming SQL queries
    that run on a schedule and insert results into target streams.
    
    Example:
        >>> task_manager = TaskManager(client)
        >>> task_manager.create_heartbeat_task(interval_minutes=30)
    """
    
    def __init__(self, client: "TimeplusClient"):
        """Initialize task manager.
        
        Args:
            client: Timeplus client instance
        """
        self.client = client
    
    def create_task(
        self,
        name: str,
        schedule: str,
        query: str,
        target_stream: str,
        timeout_seconds: int = 60,
    ) -> None:
        """Create a scheduled task.
        
        Args:
            name: Task name (must be unique)
            schedule: Schedule expression (e.g., '30m', '1h', or CRON '0 9 * * *')
            query: SELECT query to execute
            target_stream: Stream to insert results into
            timeout_seconds: Maximum execution time
        """
        # Determine schedule type
        if schedule.startswith("CRON"):
            schedule_clause = f"SCHEDULE {schedule}"
        else:
            schedule_clause = f"SCHEDULE {schedule}"
        
        sql = f"""
            CREATE TASK IF NOT EXISTS {name}
            {schedule_clause}
            TIMEOUT {timeout_seconds}s
            INTO {target_stream}
            AS
            {query}
        """
        
        self.client.execute(sql)
        logger.info(
            "Created task",
            extra={"name": name, "schedule": schedule, "target": target_stream}
        )
    
    def drop_task(self, name: str) -> None:
        """Drop a scheduled task.
        
        Args:
            name: Task name to drop
        """
        self.client.execute(f"DROP TASK IF EXISTS {name}")
        logger.info("Dropped task", extra={"name": name})
    
    def list_tasks(self) -> list[dict[str, Any]]:
        """List all scheduled tasks.
        
        Returns:
            List of task information dictionaries
        """
        return self.client.query("SHOW TASKS")
    
    def pause_task(self, name: str) -> None:
        """Pause a scheduled task.
        
        Args:
            name: Task name to pause
        """
        self.client.execute(f"STOP TASK {name}")
        logger.info("Paused task", extra={"name": name})
    
    def resume_task(self, name: str) -> None:
        """Resume a paused task.
        
        Args:
            name: Task name to resume
        """
        self.client.execute(f"START TASK {name}")
        logger.info("Resumed task", extra={"name": name})
    
    def create_heartbeat_task(
        self,
        interval_minutes: int = 30,
        checks: list[str] | None = None,
    ) -> None:
        """Create the standard heartbeat task.
        
        Args:
            interval_minutes: Interval between heartbeats
            checks: Actions to include in heartbeat
        """
        if checks is None:
            checks = ["calendar", "reminders"]
        
        checks_array = ", ".join(f"'{c}'" for c in checks)
        
        query = f"""
            SELECT
                uuid() as id,
                now64(3) as timestamp,
                'system' as source,
                'agent' as target,
                uuid() as session_id,
                'heartbeat' as message_type,
                concat('{{"action": "proactive_check", "checks": [', '{checks_array}', ']}}') as content,
                'system' as user_id,
                '' as channel_metadata,
                0 as priority
        """
        
        self.create_task(
            name="heartbeat_task",
            schedule=f"{interval_minutes}m",
            query=query,
            target_stream="messages",
            timeout_seconds=10,
        )
    
    def create_daily_summary_task(
        self,
        cron: str = "0 9 * * *",
        include: list[str] | None = None,
    ) -> None:
        """Create the daily summary task.
        
        Args:
            cron: Cron expression for scheduling
            include: Items to include in summary
        """
        if include is None:
            include = ["calendar", "weather", "news", "reminders"]
        
        include_array = ", ".join(f"'{i}'" for i in include)
        
        query = f"""
            SELECT
                uuid() as id,
                now64(3) as timestamp,
                'system' as source,
                'agent' as target,
                uuid() as session_id,
                'scheduled_task' as message_type,
                concat('{{"action": "generate_daily_briefing", "include": [', '{include_array}', ']}}') as content,
                'system' as user_id,
                '' as channel_metadata,
                1 as priority
        """
        
        self.create_task(
            name="daily_summary",
            schedule=f"CRON '{cron}'",
            query=query,
            target_stream="messages",
            timeout_seconds=60,
        )
    
    def create_cost_alert_task(
        self,
        threshold_usd: float = 5.0,
    ) -> None:
        """Create cost monitoring alert task.
        
        Args:
            threshold_usd: Hourly cost threshold for warnings
        """
        query = f"""
            SELECT
                uuid() as id,
                now64(3) as timestamp,
                'cost_alert' as event_type,
                'llm_monitor' as source,
                if(hourly_cost > {threshold_usd}, 'warning', 'info') as severity,
                concat('{{"hourly_cost_usd": ', to_string(hourly_cost), ', "request_count": ', to_string(req_count), '}}') as payload,
                ['cost', 'llm'] as tags
            FROM (
                SELECT 
                    sum(estimated_cost_usd) as hourly_cost,
                    count() as req_count
                FROM table(llm_logs)
                WHERE timestamp > now() - interval 1 hour
            )
        """
        
        self.create_task(
            name="cost_alert",
            schedule="1h",
            query=query,
            target_stream="events",
            timeout_seconds=5,
        )
