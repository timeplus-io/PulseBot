"""Timeplus task management for PulseBot."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)

_INTERVAL_UDF_TEMPLATE = """
CREATE OR REPLACE FUNCTION trigger_pulsebot_task(
    task_id string, task_name string, prompt string
) RETURNS string LANGUAGE PYTHON AS $$
import requests

def trigger_pulsebot_task(task_id, task_name, prompt):
    try:
        resp = requests.post(
            '{api_url}/api/v1/task-trigger',
            json={{
                'task_id': task_id[0],
                'task_name': task_name[0],
                'prompt': prompt[0],
                'trigger_type': 'interval',
            }},
            timeout=10,
        )
        data = resp.json()
        return [data.get('execution_id', '')]
    except Exception as e:
        return [f'error: {{str(e)}}']
$$
"""

_CRON_UDF_TEMPLATE = """
CREATE OR REPLACE FUNCTION check_cron_and_trigger(
    task_id string, task_name string, prompt string, cron_expr string
) RETURNS string LANGUAGE PYTHON AS $$
from datetime import datetime

def _matches_field(field, value):
    if field == '*':
        return True
    for part in field.split(','):
        if '/' in part:
            base, step = part.split('/', 1)
            start = 0 if base == '*' else int(base)
            if value >= start and (value - start) % int(step) == 0:
                return True
        elif '-' in part:
            lo, hi = part.split('-', 1)
            if int(lo) <= value <= int(hi):
                return True
        elif int(part) == value:
            return True
    return False

def _matches_cron(expr, now):
    parts = expr.split()
    if len(parts) != 5:
        return False
    minute, hour, dom, month, dow = parts
    return (
        _matches_field(minute, now.minute) and
        _matches_field(hour, now.hour) and
        _matches_field(dom, now.day) and
        _matches_field(month, now.month) and
        _matches_field(dow, now.weekday())
    )

def check_cron_and_trigger(task_id, task_name, prompt, cron_expr):
    now = datetime.now()
    if not _matches_cron(cron_expr[0], now):
        return ['skipped']
    try:
        import requests
        resp = requests.post(
            '{api_url}/api/v1/task-trigger',
            json={{
                'task_id': task_id[0],
                'task_name': task_name[0],
                'prompt': prompt[0],
                'trigger_type': 'cron',
                'cron_expression': cron_expr[0],
            }},
            timeout=10,
        )
        data = resp.json()
        return [data.get('execution_id', '')]
    except Exception as e:
        return [f'error: {{str(e)}}']
$$
"""


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
            extra={"task_name": name, "schedule": schedule, "target": target_stream}
        )
    
    def _write_task_status(
        self,
        name: str,
        status: str,
        task_type: str = "",
        prompt: str = "",
        schedule: str = "",
    ) -> None:
        """Append a status record to pulsebot.tasks for tracking."""
        self.client.insert(
            "pulsebot.tasks",
            [{"task_name": name, "task_type": task_type, "prompt": prompt,
              "schedule": schedule, "status": status}],
        )

    def drop_task(self, name: str) -> None:
        """Drop a scheduled task.

        Args:
            name: Task name to drop
        """
        self.client.execute(f"DROP TASK IF EXISTS {name}")
        self._write_task_status(name, "deleted")
        logger.info("Dropped task", extra={"task_name": name})

    def list_tasks(self) -> list[dict[str, Any]]:
        """List user-created tasks with their current status from pulsebot.tasks.

        Returns the latest status record per task, excluding deleted tasks.
        Falls back to SHOW TASKS if the tasks stream is unavailable.

        Returns:
            List of task information dictionaries with keys: name, status, schedule.
        """
        try:
            rows = self.client.query(
                "SELECT name, status, schedule FROM ("
                "  SELECT task_name AS name,"
                "         arg_max(status,   created_at) AS status,"
                "         arg_max(schedule, created_at) AS schedule"
                "  FROM table(pulsebot.tasks)"
                "  GROUP BY task_name"
                ") WHERE status != 'deleted'"
            )
            return rows
        except Exception as e:
            logger.warning("list_tasks query failed, falling back to SHOW TASKS: %s", e)
            return self.client.query("SHOW TASKS")

    def pause_task(self, name: str) -> None:
        """Pause a scheduled task.

        Args:
            name: Task name to pause
        """
        self.client.execute(f"SYSTEM PAUSE TASK {name}")
        self._write_task_status(name, "paused")
        logger.info("Paused task", extra={"task_name": name})

    def resume_task(self, name: str) -> None:
        """Resume a paused task.

        Args:
            name: Task name to resume
        """
        self.client.execute(f"SYSTEM RESUME TASK {name}")
        self._write_task_status(name, "active")
        logger.info("Resumed task", extra={"task_name": name})
    
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
            target_stream="pulsebot.messages",
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
            target_stream="pulsebot.messages",
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
                FROM table(pulsebot.llm_logs)
                WHERE timestamp > now() - interval 1 hour
            )
        """
        
        self.create_task(
            name="cost_alert",
            schedule="1h",
            query=query,
            target_stream="pulsebot.events",
            timeout_seconds=5,
        )

    @staticmethod
    def _sanitise_task_name(name: str) -> str:
        """Lowercase, replace non-alnum runs with underscore, add 'user_' prefix."""
        safe = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        return f"user_{safe}"

    def create_interval_task(
        self,
        name: str,
        prompt: str,
        interval: str,
        api_url: str = "http://localhost:8000",
    ) -> str:
        """Create an interval-based task using a Timeplus Python UDF.

        The task fires on the given interval, invoking the
        ``trigger_pulsebot_task`` UDF which POSTs to the PulseBot
        ``/api/v1/task-trigger`` endpoint.

        Args:
            name: Human-readable task name (will be sanitised).
            prompt: Instruction for the agent to execute each run.
            interval: Timeplus interval string, e.g. ``"15m"`` or ``"1h"``.
            api_url: Base URL of the PulseBot API server.

        Returns:
            The sanitised internal task name.
        """
        task_name = self._sanitise_task_name(name)
        safe_prompt = prompt.replace("'", "''")

        # 1. Create the Python UDF
        udf_sql = _INTERVAL_UDF_TEMPLATE.format(api_url=api_url)
        self.client.execute(udf_sql)

        # 2. Create the Timeplus TASK
        task_sql = f"""
            CREATE TASK IF NOT EXISTS {task_name}
            SCHEDULE {interval}
            TIMEOUT 30s
            INTO pulsebot.task_triggers
            AS
            SELECT
                uuid()                                                AS trigger_id,
                '{task_name}'                                         AS task_id,
                '{task_name}'                                         AS task_name,
                '{safe_prompt}'                                       AS prompt,
                trigger_pulsebot_task('{task_name}', '{task_name}', '{safe_prompt}') AS execution_id,
                now64(3)                                              AS triggered_at
        """
        self.client.execute(task_sql)
        self._write_task_status(task_name, "active", task_type="interval", prompt=prompt, schedule=interval)

        logger.info("Created interval task", extra={"task_name": task_name, "interval": interval})
        return task_name

    def create_cron_task(
        self,
        name: str,
        prompt: str,
        cron: str,
        api_url: str = "http://localhost:8000",
    ) -> str:
        """Create a cron-scheduled task using a 1-minute polling Timeplus Task.

        The task polls every minute and uses the ``check_cron_and_trigger``
        Python UDF to match the cron expression and conditionally POST to
        the PulseBot ``/api/v1/task-trigger`` endpoint.

        Args:
            name: Human-readable task name (will be sanitised).
            prompt: Instruction for the agent to execute each run.
            cron: Standard 5-field cron expression, e.g. ``"0 8 * * *"``.
            api_url: Base URL of the PulseBot API server.

        Returns:
            The sanitised internal task name.
        """
        task_name = self._sanitise_task_name(name)
        safe_prompt = prompt.replace("'", "''")
        safe_cron = cron.replace("'", "''")

        # 1. Create the cron-matching Python UDF
        udf_sql = _CRON_UDF_TEMPLATE.format(api_url=api_url)
        self.client.execute(udf_sql)

        # 2. Create the 1-minute polling TASK
        task_sql = f"""
            CREATE TASK IF NOT EXISTS {task_name}
            SCHEDULE 1m
            TIMEOUT 30s
            INTO pulsebot.task_triggers
            AS
            SELECT
                uuid()                                                                AS trigger_id,
                '{task_name}'                                                         AS task_id,
                '{task_name}'                                                         AS task_name,
                '{safe_prompt}'                                                       AS prompt,
                check_cron_and_trigger('{task_name}', '{task_name}', '{safe_prompt}', '{safe_cron}') AS execution_id,
                now64(3)                                                              AS triggered_at
        """
        self.client.execute(task_sql)
        self._write_task_status(task_name, "active", task_type="cron", prompt=prompt, schedule=cron)

        logger.info("Created cron task", extra={"task_name": task_name, "cron": cron})
        return task_name
