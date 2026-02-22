"""WorkspaceServer — embedded HTTP server that runs inside the agent process.

Serves:
  - Static file artifacts
  - HTML app frontends (index.html)
  - Proton streaming SQL proxy (POST /query) — avoids browser CORS limits
  - Reverse-proxy to backend subprocesses (/api/* per task)

Runs on workspace_port (default 8001). Starts automatically with the agent.
Only reachable from the API server on the internal network.

Routes
------
  GET   /health
  POST  /query                              → Proton:3218 streaming proxy
  GET   /{session_id}/list
  GET   /{session_id}/{task_id}/
  GET   /{session_id}/{task_id}/index.html
  ANY   /{session_id}/{task_id}/api/{path} → backend subprocess proxy
  GET   /{session_id}/{task_id}/{path}     → static file

Proton query proxy
------------------
Frontend apps call:

  const resp = await fetch('http://localhost:8001/query', {
    method: 'POST',
    body: 'SELECT * FROM my_stream'
  });
  for await (const row of parseNDJSON(resp.body.getReader())) { ... }

Auth is passed as HTTP Basic using the existing Timeplus credentials
(TIMEPLUS_USER / TIMEPLUS_PASSWORD) — no separate config needed.
"""

from __future__ import annotations

import base64
import asyncio
from typing import Any, AsyncIterator

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
    proton_username: str = "default",
    proton_password: str = "",
    proton_host: str = "localhost",
) -> FastAPI:
    """Build the FastAPI application for the agent's WorkspaceServer.

    Args:
        manager: WorkspaceManager instance (shared with WorkspaceSkill).
        config: WorkspaceConfig (for port, base_dir, proton_url).
        proton_username: Proton HTTP auth username (from cfg.timeplus.username).
        proton_password: Proton HTTP auth password (from cfg.timeplus.password).
    """
    app = FastAPI(
        title="PulseBot WorkspaceServer",
        description="Agent-side file server, backend proxy, and Proton query proxy",
        docs_url=None,
        redoc_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Build Proton auth header once at startup — reused on every query
    _proton_url = f"http://{proton_host}:3218"
    _proton_headers: dict[str, str] = {"Content-Type": "text/plain"}
    if proton_username:
        creds = base64.b64encode(f"{proton_username}:{proton_password}".encode()).decode()
        _proton_headers["Authorization"] = f"Basic {creds}"

    # ── health ────────────────────────────────────────────────────────────

    @app.get("/health")
    async def health() -> JSONResponse:
        return JSONResponse({
            "status": "ok",
            "service": "workspace-server",
            "proton_url": _proton_url,
        })

    # ── Proton streaming SQL proxy ────────────────────────────────────────
    #
    # POST /query  — accepts raw SQL in body, streams NDJSON back.
    # Mirrors proxy.ts exactly (same path, same protocol).
    # Auth uses TIMEPLUS_USER / TIMEPLUS_PASSWORD via proton_username/password args.

    @app.post("/query")
    async def proton_query(request: Request) -> StreamingResponse:
        """Proxy raw SQL to Proton and stream NDJSON results back."""
        body = await request.body()
        sql = body.decode(errors="replace").strip()
        fmt = request.query_params.get("default_format", "JSONEachRow")

        if not sql:
            raise HTTPException(status_code=400, detail="Request body must be a SQL query string.")

        target = f"{_proton_url.rstrip('/')}/?default_format={fmt}"
        logger.debug(f"[workspace] /query sql={sql[:80]!r} → {_proton_url}")

        async def stream() -> AsyncIterator[bytes]:
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream(
                        "POST",
                        target,
                        content=sql.encode(),
                        headers=_proton_headers,
                    ) as resp:
                        if resp.status_code != 200:
                            error_body = await resp.aread()
                            logger.warning(
                                f"[workspace] Proton error {resp.status_code}: "
                                f"{error_body.decode()[:300]}"
                            )
                            yield error_body
                            return
                        async for chunk in resp.aiter_bytes():
                            yield chunk
            except httpx.ConnectError as exc:
                logger.error(f"[workspace] Proton unreachable at {_proton_url}: {exc}")
                import json
                yield json.dumps({
                    "error": f"Proton is unreachable at {_proton_url}."
                }).encode()

        return StreamingResponse(
            content=stream(),
            media_type="application/x-ndjson",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

    # ── session task listing ──────────────────────────────────────────────

    @app.get("/{session_id}/list")
    async def list_tasks(session_id: str) -> JSONResponse:
        tasks = manager.list_tasks(session_id)
        return JSONResponse({"session_id": session_id, "tasks": tasks})

    # ── app index ─────────────────────────────────────────────────────────

    @app.get("/{session_id}/{task_id}/")
    @app.get("/{session_id}/{task_id}/index.html")
    async def serve_index(session_id: str, task_id: str) -> FileResponse:
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
        """Reverse-proxy /api/* requests to the task's backend subprocess."""
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
    # Must be last — broadest route.

    @app.get("/{session_id}/{task_id}/{file_path:path}")
    async def serve_file(
        session_id: str, task_id: str, file_path: str
    ) -> FileResponse:
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
    proton_username: str = "default",
    proton_password: str = "",
    proton_host: str = "localhost",
) -> None:
    """Start the WorkspaceServer using uvicorn.

    Args:
        manager: Shared WorkspaceManager instance.
        config: WorkspaceConfig with workspace_port.
        proton_username: From cfg.timeplus.username (TIMEPLUS_USER).
        proton_password: From cfg.timeplus.password (TIMEPLUS_PASSWORD).
        proton_host: From cfg.timeplus.host (TIMEPLUS_HOST).
    """
    app = create_workspace_server(manager, config, proton_username, proton_password, proton_host)

    server_config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=config.workspace_port,
        log_level="warning",
        access_log=False,
    )
    server = uvicorn.Server(server_config)

    logger.info(
        f"[workspace] WorkspaceServer starting on port {config.workspace_port} "
        f"(Proton proxy → {proton_host}:3218 user={proton_username})"
    )
    await server.serve()