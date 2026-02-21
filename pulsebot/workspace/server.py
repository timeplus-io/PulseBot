"""WorkspaceServer — embedded HTTP server that runs inside the agent process.

Serves:
  - Static file artifacts
  - HTML app frontends (index.html)
  - Reverse-proxy to backend subprocesses (/api/* paths)

Runs on workspace_port (default 8001). Starts automatically with the agent.
Only reachable from the API server on the internal network — never exposed
to the public internet directly.

Routes
------
  GET  /health
  GET  /{session_id}/list
  GET  /{session_id}/{task_id}/
  GET  /{session_id}/{task_id}/index.html
  GET  /{session_id}/{task_id}/{file_path}
  ANY  /{session_id}/{task_id}/api/{api_path}   → proxy to backend subprocess
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from pulsebot.utils import get_logger
from pulsebot.workspace.config import WorkspaceConfig
from pulsebot.workspace.manager import WorkspaceManager

logger = get_logger(__name__)


def create_workspace_server(
    manager: WorkspaceManager,
    config: WorkspaceConfig,
) -> FastAPI:
    """Build the FastAPI application for the agent's WorkspaceServer.

    Args:
        manager: WorkspaceManager instance (shared with WorkspaceSkill).
        config: WorkspaceConfig (for port and base_dir).

    Returns:
        Configured FastAPI app ready to be run by uvicorn.
    """
    app = FastAPI(
        title="PulseBot WorkspaceServer",
        description="Agent-side file server and backend proxy",
        docs_url=None,
        redoc_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── health ────────────────────────────────────────────────────────────

    @app.get("/health")
    async def health() -> JSONResponse:
        return JSONResponse({"status": "ok", "service": "workspace-server"})

    # ── session task listing ──────────────────────────────────────────────

    @app.get("/{session_id}/list")
    async def list_tasks(session_id: str) -> JSONResponse:
        """List all tasks in a session with their status."""
        tasks = manager.list_tasks(session_id)
        return JSONResponse({"session_id": session_id, "tasks": tasks})

    # ── app index ─────────────────────────────────────────────────────────

    @app.get("/{session_id}/{task_id}/")
    @app.get("/{session_id}/{task_id}/index.html")
    async def serve_index(session_id: str, task_id: str) -> FileResponse:
        """Serve index.html for an app task."""
        f = manager.resolve_task_file(session_id, task_id, "index.html")
        if f is None:
            raise HTTPException(
                status_code=404,
                detail=f"No app found for task '{task_id}' in session '{session_id}'.",
            )
        return FileResponse(str(f))

    # ── backend API proxy ─────────────────────────────────────────────────

    @app.api_route(
        "/{session_id}/{task_id}/api/{api_path:path}",
        methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    )
    async def proxy_backend(
        session_id: str,
        task_id: str,
        api_path: str,
        request: Request,
    ) -> Any:
        """Reverse-proxy /api/* requests to the task's backend subprocess.

        The subprocess listens on 127.0.0.1:{port}. It is never reachable
        except through this proxy.
        """
        port = manager.get_backend_port(session_id, task_id)
        if port is None:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"No backend is running for task '{task_id}'. "
                    "Use workspace_start_app to start it."
                ),
            )

        body = await request.body()
        qs = request.url.query
        upstream = f"http://127.0.0.1:{port}/api/{api_path}"
        if qs:
            upstream += f"?{qs}"

        fwd_headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ("host", "content-length")
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.request(
                    method=request.method,
                    url=upstream,
                    headers=fwd_headers,
                    content=body,
                )
            return StreamingResponse(
                content=resp.aiter_bytes(),
                status_code=resp.status_code,
                headers=dict(resp.headers),
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=502,
                detail=(
                    f"Backend for task '{task_id}' is unreachable — it may have crashed. "
                    "Check backend.log or use workspace_start_app to restart."
                ),
            )

    # ── static file serving ───────────────────────────────────────────────
    # Must be last — broadest route, catches everything not matched above.

    @app.get("/{session_id}/{task_id}/{file_path:path}")
    async def serve_file(
        session_id: str, task_id: str, file_path: str
    ) -> FileResponse:
        """Serve any static artifact from the task directory."""
        f = manager.resolve_task_file(session_id, task_id, file_path)
        if f is None:
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {file_path}",
            )
        return FileResponse(str(f))

    return app


async def run_workspace_server(
    manager: WorkspaceManager,
    config: WorkspaceConfig,
) -> None:
    """Start the WorkspaceServer using uvicorn.

    Designed to run as an asyncio task alongside the agent:

        asyncio.create_task(run_workspace_server(manager, cfg.workspace))

    Args:
        manager: Shared WorkspaceManager instance.
        config: WorkspaceConfig with workspace_port.
    """
    app = create_workspace_server(manager, config)

    server_config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=config.workspace_port,
        log_level="warning",
        access_log=False,
    )
    server = uvicorn.Server(server_config)

    logger.info(
        f"[workspace] WorkspaceServer starting on port {config.workspace_port}"
    )
    await server.serve()
