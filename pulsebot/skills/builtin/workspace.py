"""WorkspaceSkill — agent-side builtin skill for the Agent Workspace feature.

Location: pulsebot/skills/builtin/workspace.py
Registered: BUILTIN_SKILLS in loader.py  (same as web_search, file_ops, shell)
Instantiated: create_skill_loader() in factory.py

How it works
------------
  1. LLM calls a workspace tool (e.g. workspace_create_fullstack_app).
  2. WorkspaceSkill calls WorkspaceManager to write files and start subprocesses
     — all local, no network needed.
  3. WorkspaceSkill calls ProxyRegistryClient to POST /internal/workspace/register
     on the API server — the only HTTP call the agent makes for workspace.
  4. WorkspaceSkill builds the public URL from base_url + session + task_id
     and returns it to the LLM as a shareable link for the user.

Tools
-----
  workspace_write_file
  workspace_create_app
  workspace_create_fullstack_app
  workspace_start_app
  workspace_stop_app
  workspace_delete_task
  workspace_list_tasks
"""

from __future__ import annotations

import textwrap
from typing import Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger
from pulsebot.workspace.config import WorkspaceConfig
from pulsebot.workspace.manager import WorkspaceManager
from pulsebot.workspace.registry_client import ProxyRegistryClient

logger = get_logger(__name__)


class WorkspaceSkill(BaseSkill):
    """LLM-facing workspace skill.

    Registered in loader.py's BUILTIN_SKILLS and instantiated by
    create_skill_loader() in factory.py which injects WorkspaceConfig.

    Args:
        config: WorkspaceConfig from cfg.workspace.

    Example::

        skill = WorkspaceSkill(config=cfg.workspace)
    """

    name = "workspace"
    description = (
        "Create and publish file artifacts and runnable web apps "
        "as shareable URLs accessible from the API server."
    )

    def __init__(self, config: WorkspaceConfig) -> None:
        self._cfg = config
        self._manager = WorkspaceManager(config)
        self._registry_client = ProxyRegistryClient(config)

    @property
    def manager(self) -> WorkspaceManager:
        """Expose the WorkspaceManager so cli.py can pass it to WorkspaceServer."""
        return self._manager

    # ── URL construction ──────────────────────────────────────────────────

    def _public_url(self, session_id: str, task_id: str) -> str:
        base = self._cfg.api_server_url.rstrip("/")
        return f"{base}/workspace/{session_id}/{task_id}/"

    # ── tool definitions ──────────────────────────────────────────────────

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="workspace_write_file",
                description=(
                    "Write a static artifact (CSV, Markdown, HTML, JSON, Python script, etc.) "
                    "to the agent workspace and return a shareable URL. "
                    "Use for any output the user should be able to download or view."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Current conversation session ID.",
                        },
                        "task_name": {
                            "type": "string",
                            "description": (
                                "Human-readable name for this task, e.g. 'Q3 Sales Report'. "
                                "Used to generate a URL-friendly task ID."
                            ),
                        },
                        "file_name": {
                            "type": "string",
                            "description": "Filename, e.g. 'report.csv', 'summary.md'.",
                        },
                        "content": {
                            "type": "string",
                            "description": "Full text content of the file.",
                        },
                    },
                    "required": ["session_id", "task_name", "file_name", "content"],
                },
            ),
            ToolDefinition(
                name="workspace_create_app",
                description=(
                    "Create a self-contained HTML web app and return a shareable URL. "
                    "Use for interactive charts, dashboards, calculators, or any browser-based "
                    "tool that needs no server-side logic. "
                    "The HTML may use inline CSS/JS and CDN-hosted libraries."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Current conversation session ID.",
                        },
                        "task_name": {
                            "type": "string",
                            "description": "Human-readable name, e.g. 'CPU Usage Chart'.",
                        },
                        "html": {
                            "type": "string",
                            "description": (
                                "Complete self-contained HTML (<!DOCTYPE html> … </html>). "
                                "Inline all CSS and JS. CDN links are fine. "
                                "No references to external files."
                            ),
                        },
                    },
                    "required": ["session_id", "task_name", "html"],
                },
            ),
            ToolDefinition(
                name="workspace_create_fullstack_app",
                description=(
                    "Create a web app with an HTML frontend and a Python (FastAPI) backend. "
                    "Use when the app needs server-side logic, real-time data, or database access. "
                    "The backend runs as a subprocess on the agent machine; its API is accessible "
                    "at /workspace/{session_id}/{task_id}/api/..."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Current conversation session ID.",
                        },
                        "task_name": {
                            "type": "string",
                            "description": "Human-readable name, e.g. 'Live CPU Monitor'.",
                        },
                        "html": {
                            "type": "string",
                            "description": textwrap.dedent("""\
                                Frontend HTML. All API calls must target the proxy path:
                                  /workspace/{session_id}/{task_id}/api/...
                                Replace {session_id} and {task_id} with the actual values
                                (task_id is returned in the tool result).
                                Use a JS variable or fetch wrapper so the base path is easy
                                to configure, e.g.:
                                  const API = `/workspace/SESSION/TASK/api`;
                                  fetch(`${API}/data`)
                            """),
                        },
                        "backend_py": {
                            "type": "string",
                            "description": textwrap.dedent("""\
                                Python source for the FastAPI backend.
                                MUST read PORT from os.environ and start uvicorn on 127.0.0.1.
                                All routes must be under /api/ prefix.

                                Minimal template:
                                  import os
                                  import uvicorn
                                  from fastapi import FastAPI
                                  from fastapi.middleware.cors import CORSMiddleware

                                  app = FastAPI()
                                  app.add_middleware(CORSMiddleware, allow_origins=["*"],
                                      allow_methods=["*"], allow_headers=["*"])

                                  @app.get("/api/ping")
                                  def ping(): return {"ok": True}

                                  if __name__ == "__main__":
                                      port = int(os.environ.get("PORT", 8001))
                                      uvicorn.run(app, host="127.0.0.1", port=port)
                            """),
                        },
                        "requirements": {
                            "type": "string",
                            "description": (
                                "Optional pip packages, one per line. "
                                "fastapi and uvicorn are always available."
                            ),
                        },
                    },
                    "required": ["session_id", "task_name", "html", "backend_py"],
                },
            ),
            ToolDefinition(
                name="workspace_start_app",
                description=(
                    "Start or restart the Python backend for an existing fullstack app task. "
                    "Use after workspace_create_fullstack_app, or to restart a crashed backend."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Current conversation session ID.",
                        },
                        "task_id": {
                            "type": "string",
                            "description": "Task ID returned by workspace_create_fullstack_app.",
                        },
                    },
                    "required": ["session_id", "task_id"],
                },
            ),
            ToolDefinition(
                name="workspace_stop_app",
                description=(
                    "Stop the running Python backend for a task. "
                    "Files are preserved; the task stays registered. "
                    "Use workspace_start_app to restart later."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Current conversation session ID.",
                        },
                        "task_id": {
                            "type": "string",
                            "description": "Task ID of the app to stop.",
                        },
                    },
                    "required": ["session_id", "task_id"],
                },
            ),
            ToolDefinition(
                name="workspace_delete_task",
                description=(
                    "Permanently delete a workspace task: stops the backend (if running), "
                    "deletes all files, and deregisters the public URL. Irreversible."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Current conversation session ID.",
                        },
                        "task_id": {
                            "type": "string",
                            "description": "Task ID to delete.",
                        },
                    },
                    "required": ["session_id", "task_id"],
                },
            ),
            ToolDefinition(
                name="workspace_list_tasks",
                description=(
                    "List all workspace tasks in the current session with their "
                    "status, artifact type, and public URL."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Current conversation session ID.",
                        },
                    },
                    "required": ["session_id"],
                },
            ),
        ]

    # ── execution dispatch ────────────────────────────────────────────────

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        session_id = arguments.get("session_id", "").strip()
        if not session_id:
            return ToolResult.fail("session_id is required")

        handlers = {
            "workspace_write_file": self._handle_write_file,
            "workspace_create_app": self._handle_create_app,
            "workspace_create_fullstack_app": self._handle_create_fullstack_app,
            "workspace_start_app": self._handle_start_app,
            "workspace_stop_app": self._handle_stop_app,
            "workspace_delete_task": self._handle_delete_task,
            "workspace_list_tasks": self._handle_list_tasks,
        }
        handler = handlers.get(tool_name)
        if handler is None:
            return ToolResult.fail(f"Unknown workspace tool: {tool_name}")

        try:
            return await handler(session_id, arguments)
        except Exception as exc:
            logger.error(f"[workspace] {tool_name} failed: {exc}", exc_info=True)
            return ToolResult.fail(str(exc))

    # ── handlers ───────────────────────────────────────────────────────────

    async def _handle_write_file(
        self, session_id: str, args: dict[str, Any]
    ) -> ToolResult:
        task_name = args.get("task_name", "").strip()
        file_name = args.get("file_name", "").strip()
        content = args.get("content", "")

        if not task_name:
            return ToolResult.fail("task_name is required")
        if not file_name:
            return ToolResult.fail("file_name is required")

        task_id = self._manager.create_task(session_id, task_name, "file")
        written = self._manager.write_task_file(session_id, task_id, file_name, content)

        reg = await self._registry_client.register(session_id, task_id, "file")
        public_url = self._public_url(session_id, task_id) + file_name

        logger.info(f"[workspace] file ready session={session_id} task={task_id} file={file_name}")
        return ToolResult.ok({
            "status": "created",
            "task_id": task_id,
            "file_name": file_name,
            "public_url": public_url,
            "bytes_written": len(content.encode()),
            "message": f"File available at: {public_url}",
        })

    async def _handle_create_app(
        self, session_id: str, args: dict[str, Any]
    ) -> ToolResult:
        task_name = args.get("task_name", "").strip()
        html = args.get("html", "").strip()

        if not task_name:
            return ToolResult.fail("task_name is required")
        if not html:
            return ToolResult.fail("html is required")

        task_id = self._manager.create_task(session_id, task_name, "html_app")
        self._manager.write_task_file(session_id, task_id, "index.html", html)

        await self._registry_client.register(session_id, task_id, "html_app")
        public_url = self._public_url(session_id, task_id)

        logger.info(f"[workspace] html app ready session={session_id} task={task_id}")
        return ToolResult.ok({
            "status": "created",
            "task_id": task_id,
            "public_url": public_url,
            "message": f"App is live at: {public_url}",
        })

    async def _handle_create_fullstack_app(
        self, session_id: str, args: dict[str, Any]
    ) -> ToolResult:
        task_name = args.get("task_name", "").strip()
        html = args.get("html", "").strip()
        backend_py = args.get("backend_py", "").strip()
        requirements = args.get("requirements", "").strip()

        if not task_name:
            return ToolResult.fail("task_name is required")
        if not html:
            return ToolResult.fail("html is required")
        if not backend_py:
            return ToolResult.fail("backend_py is required")

        task_id = self._manager.create_task(session_id, task_name, "fullstack_app")

        # Write all files to the workspace directory
        self._manager.write_task_file(session_id, task_id, "index.html", html)
        self._manager.write_task_file(session_id, task_id, "backend.py", backend_py)
        if requirements:
            self._manager.write_task_file(
                session_id, task_id, "requirements.txt", requirements
            )

        # Start the backend subprocess
        port = await self._manager.start_backend(session_id, task_id)

        # Register with API server
        await self._registry_client.register(session_id, task_id, "fullstack_app")
        public_url = self._public_url(session_id, task_id)

        logger.info(
            f"[workspace] fullstack app ready session={session_id} "
            f"task={task_id} port={port}"
        )
        return ToolResult.ok({
            "status": "created_and_started",
            "task_id": task_id,
            "public_url": public_url,
            "backend_port": port,
            "message": (
                f"Full-stack app is live at: {public_url}\n"
                f"Frontend calls to /workspace/{session_id}/{task_id}/api/... "
                f"are proxied to the backend."
            ),
        })

    async def _handle_start_app(
        self, session_id: str, args: dict[str, Any]
    ) -> ToolResult:
        task_id = args.get("task_id", "").strip()
        if not task_id:
            return ToolResult.fail("task_id is required")

        try:
            port = await self._manager.start_backend(session_id, task_id)
        except FileNotFoundError as exc:
            return ToolResult.fail(str(exc))
        except RuntimeError as exc:
            return ToolResult.fail(str(exc))

        public_url = self._public_url(session_id, task_id)
        return ToolResult.ok({
            "status": "started",
            "task_id": task_id,
            "public_url": public_url,
            "backend_port": port,
            "message": f"Backend (re)started. App at: {public_url}",
        })

    async def _handle_stop_app(
        self, session_id: str, args: dict[str, Any]
    ) -> ToolResult:
        task_id = args.get("task_id", "").strip()
        if not task_id:
            return ToolResult.fail("task_id is required")

        await self._manager.stop_backend(session_id, task_id)
        return ToolResult.ok({
            "status": "stopped",
            "task_id": task_id,
            "message": "Backend stopped. Files preserved. Use workspace_start_app to restart.",
        })

    async def _handle_delete_task(
        self, session_id: str, args: dict[str, Any]
    ) -> ToolResult:
        task_id = args.get("task_id", "").strip()
        if not task_id:
            return ToolResult.fail("task_id is required")

        await self._manager.delete_task(session_id, task_id)

        try:
            await self._registry_client.deregister(session_id, task_id)
        except Exception as exc:
            logger.warning(
                f"[workspace] deregister failed for {session_id}/{task_id}: {exc}"
            )

        return ToolResult.ok({
            "status": "deleted",
            "task_id": task_id,
            "message": f"Task '{task_id}' and all its files have been permanently deleted.",
        })

    async def _handle_list_tasks(
        self, session_id: str, args: dict[str, Any]
    ) -> ToolResult:
        tasks = self._manager.list_tasks(session_id)

        # Enrich with public URLs
        for t in tasks:
            t["public_url"] = self._public_url(session_id, t["task_id"])

        return ToolResult.ok({
            "count": len(tasks),
            "tasks": tasks,
        })
