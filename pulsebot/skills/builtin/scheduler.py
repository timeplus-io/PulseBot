"""SchedulerSkill — lets the LLM create and manage user-defined recurring tasks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.tasks import TaskManager

logger = get_logger(__name__)


class SchedulerSkill(BaseSkill):
    """LLM-callable tools for creating and managing scheduled tasks.

    Delegates to TaskManager's UDF-based methods which create Timeplus
    TASKs that POST back to /api/v1/task-trigger on each execution.
    """

    name = "scheduler"
    description = "Create and manage user-defined recurring tasks"

    def __init__(self, timeplus_config: Any, api_url: str = "http://localhost:8000"):
        from pulsebot.timeplus.client import TimeplusClient
        from pulsebot.timeplus.tasks import TaskManager
        client = TimeplusClient.from_config(timeplus_config)
        self.task_manager = TaskManager(client)
        self.api_url = api_url

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="create_interval_task",
                description=(
                    "Create a task that repeats on a fixed interval (e.g. every 15 minutes). "
                    "Use this when the user says 'every X minutes/hours' or similar."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Short task name (e.g. 'weather-report')"},
                        "prompt": {"type": "string", "description": "Instruction to execute each run"},
                        "interval": {"type": "string", "description": "Interval string, e.g. '15m', '1h', '30m'"},
                    },
                    "required": ["name", "prompt", "interval"],
                },
            ),
            ToolDefinition(
                name="create_cron_task",
                description=(
                    "Create a task on a calendar schedule (e.g. 8 AM daily). "
                    "Use this when the user specifies a time of day or day of week. "
                    "Accuracy is ±1 minute."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Short task name"},
                        "prompt": {"type": "string", "description": "Instruction to execute each run"},
                        "cron": {"type": "string", "description": "5-field cron expression, e.g. '0 8 * * *'"},
                    },
                    "required": ["name", "prompt", "cron"],
                },
            ),
            ToolDefinition(
                name="list_tasks",
                description="List all user-created scheduled tasks and their current status.",
                parameters={"type": "object", "properties": {}},
            ),
            ToolDefinition(
                name="pause_task",
                description="Pause a user-created scheduled task so it stops firing.",
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name (starts with 'user_')"},
                    },
                    "required": ["name"],
                },
            ),
            ToolDefinition(
                name="resume_task",
                description="Resume a paused user-created scheduled task.",
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name (starts with 'user_')"},
                    },
                    "required": ["name"],
                },
            ),
            ToolDefinition(
                name="delete_task",
                description="Permanently delete a user-created scheduled task.",
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name (starts with 'user_')"},
                    },
                    "required": ["name"],
                },
            ),
        ]

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        if tool_name == "create_interval_task":
            return await self._create_interval(arguments)
        if tool_name == "create_cron_task":
            return await self._create_cron(arguments)
        if tool_name == "list_tasks":
            return await self._list()
        if tool_name == "pause_task":
            return await self._lifecycle("pause", arguments)
        if tool_name == "resume_task":
            return await self._lifecycle("resume", arguments)
        if tool_name == "delete_task":
            return await self._lifecycle("delete", arguments)
        return ToolResult.fail(f"Unknown tool: {tool_name}")

    async def _create_interval(self, args: dict) -> ToolResult:
        try:
            task_name = self.task_manager.create_interval_task(
                name=args["name"],
                prompt=args["prompt"],
                interval=args["interval"],
                api_url=self.api_url,
            )
            return ToolResult.ok(
                f"Interval task '{task_name}' created. "
                f"It will run every {args['interval']} and broadcast results to all channels."
            )
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _create_cron(self, args: dict) -> ToolResult:
        try:
            task_name = self.task_manager.create_cron_task(
                name=args["name"],
                prompt=args["prompt"],
                cron=args["cron"],
                api_url=self.api_url,
            )
            return ToolResult.ok(
                f"Cron task '{task_name}' created (schedule: {args['cron']}). "
                "Results will be broadcast to all channels (±1 minute accuracy)."
            )
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _list(self) -> ToolResult:
        try:
            all_tasks = self.task_manager.list_tasks()
            user_tasks = [t for t in all_tasks if t.get("name", "").startswith("user_")]
            if not user_tasks:
                return ToolResult.ok("No user-created scheduled tasks found.")
            lines = ["User-created scheduled tasks:"]
            for t in user_tasks:
                status = t.get("status", "unknown")
                lines.append(f"  - {t['name']} ({status})")
            return ToolResult.ok("\n".join(lines))
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _lifecycle(self, action: str, args: dict) -> ToolResult:
        name = args.get("name", "")
        if not name.startswith("user_"):
            return ToolResult.fail(
                f"Cannot {action} '{name}': only user-created tasks (starting with 'user_') "
                "can be managed via this tool."
            )
        try:
            if action == "pause":
                self.task_manager.pause_task(name)
            elif action == "resume":
                self.task_manager.resume_task(name)
            elif action == "delete":
                self.task_manager.drop_task(name)
            return ToolResult.ok(f"Task '{name}' {action}d.")
        except Exception as e:
            return ToolResult.fail(str(e))
