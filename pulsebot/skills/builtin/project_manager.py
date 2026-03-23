"""Built-in skill for creating and managing multi-agent projects."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult

if TYPE_CHECKING:
    from pulsebot.agents.project_manager import ProjectManager


class ProjectManagerSkill(BaseSkill):
    """Skill that exposes multi-agent project management tools to the main agent."""

    name = "project_manager"
    description = "Create and manage multi-agent projects that decompose complex tasks"

    def __init__(self, project_manager: ProjectManager) -> None:
        self._pm = project_manager

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="create_project",
                description=(
                    "Create a new multi-agent project. Spawns a manager agent "
                    "and worker sub-agents that collaborate via a kanban stream. "
                    "Use for complex tasks that benefit from parallel or sequential "
                    "decomposition (research + analysis + writing, etc.)."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Short human-readable project name",
                        },
                        "description": {
                            "type": "string",
                            "description": "What this project aims to accomplish",
                        },
                        "agents": {
                            "type": "array",
                            "description": "Worker agent specifications",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Agent name (used to derive agent_id)"},
                                    "task_description": {"type": "string", "description": "System-level role instructions"},
                                    "target_agents": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Agent IDs that receive this agent's output. Empty = send to manager.",
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Skill names to load. Omit to inherit all main agent skills.",
                                    },
                                    "builtin_skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Builtin skills always available to this agent (default: file_ops, shell, workspace). Only applies when 'skills' is set.",
                                    },
                                    "model": {"type": "string", "description": "Override LLM model"},
                                    "provider": {"type": "string", "description": "Override LLM provider"},
                                },
                                "required": ["name", "task_description", "target_agents"],
                            },
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Current user session ID (for routing final result back to user)",
                        },
                        "initial_messages": {
                            "type": "array",
                            "description": "Initial task messages dispatched by the manager",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string", "description": "Agent ID to send task to"},
                                    "content": {"type": "string", "description": "Task content"},
                                },
                                "required": ["target", "content"],
                            },
                        },
                    },
                    "required": ["name", "description", "agents", "session_id"],
                },
            ),
            ToolDefinition(
                name="list_projects",
                description="List all active and recent multi-agent projects.",
                parameters={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["active", "completed", "failed", "cancelled"],
                            "description": "Filter by status. Omit to list all.",
                        },
                    },
                },
            ),
            ToolDefinition(
                name="cancel_project",
                description="Cancel a running multi-agent project and stop all its agents.",
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID to cancel"},
                    },
                    "required": ["project_id"],
                },
            ),
            ToolDefinition(
                name="get_project_status",
                description="Get detailed status of a specific project including all agent states.",
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID"},
                    },
                    "required": ["project_id"],
                },
            ),
            ToolDefinition(
                name="delete_project",
                description=(
                    "Cancel a project (if still running) and permanently delete all its metadata "
                    "from the projects, agents, and kanban message streams."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID to delete"},
                    },
                    "required": ["project_id"],
                },
            ),
        ]

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        try:
            if tool_name == "create_project":
                return await self._create_project(arguments)
            elif tool_name == "list_projects":
                return self._list_projects(arguments)
            elif tool_name == "cancel_project":
                return await self._cancel_project(arguments)
            elif tool_name == "get_project_status":
                return self._get_project_status(arguments)
            elif tool_name == "delete_project":
                return await self._delete_project(arguments)
            else:
                return ToolResult.fail(f"Unknown tool: {tool_name}")
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _create_project(self, args: dict) -> ToolResult:
        from pulsebot.agents.models import SubAgentSpec

        raw_agents = args.get("agents", [])
        specs = [
            SubAgentSpec(
                name=a["name"],
                task_description=a["task_description"],
                project_id="",  # set by ProjectManager
                target_agents=a.get("target_agents", []),
                skills=a.get("skills"),
                builtin_skills=a.get("builtin_skills"),
                model=a.get("model"),
                provider=a.get("provider"),
            )
            for a in raw_agents
        ]

        project_id = await self._pm.create_project(
            name=args["name"],
            description=args["description"],
            agents=specs,
            session_id=args["session_id"],
            initial_messages=args.get("initial_messages", []),
        )
        return ToolResult.ok(
            f"Project created: {project_id}\n"
            f"Spawned {len(specs)} worker agent(s). "
            f"The manager agent will deliver results to your session."
        )

    def _list_projects(self, args: dict) -> ToolResult:
        status_filter = args.get("status")
        projects = self._pm.list_projects(status=status_filter)
        if not projects:
            return ToolResult.ok("No projects found.")
        lines = ["Projects:"]
        for p in projects:
            lines.append(
                f"  [{p['status']}] {p['project_id']} — {p['name']} "
                f"({p['agent_count']} agents)"
            )
        return ToolResult.ok("\n".join(lines))

    async def _cancel_project(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        cancelled = await self._pm.cancel_project(project_id)
        if cancelled:
            return ToolResult.ok(f"Project {project_id} cancelled.")
        return ToolResult.fail(f"Project {project_id} not found.")

    def _get_project_status(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        status = self._pm.get_project_status(project_id)
        if status is None:
            return ToolResult.fail(f"Project {project_id} not found.")
        return ToolResult.ok(json.dumps(status, indent=2))

    async def _delete_project(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        deleted = await self._pm.delete_project(project_id)
        if deleted:
            return ToolResult.ok(
                f"Project {project_id} deleted. All metadata removed from projects, agents, and kanban streams."
            )
        return ToolResult.fail(f"Project {project_id} not found.")
