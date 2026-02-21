"""WorkspaceProxyRouter — API server catch-all proxy for workspace artifacts.

Handles all public workspace traffic:
  ANY /workspace/{session_id}/{task_id}/{path:path}

On each request:
  1. Look up session_id / task_id in ProxyRegistry → agent_url
  2. If not found → 404
  3. Forward request to http://{agent_host}:{workspace_port}/{session}/{task}/{path}
  4. Stream response back to the client

Wired into the FastAPI app in server.py via:
  app.include_router(workspace_proxy_router)
"""

from __future__ import annotations

from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from pulsebot.utils import get_logger
from pulsebot.workspace.proxy_registry import ProxyRegistry

logger = get_logger(__name__)

workspace_proxy_router = APIRouter(prefix="/workspace", tags=["workspace"])

# Injected once from server.py via set_proxy_registry_for_router()
_registry: ProxyRegistry | None = None


def set_proxy_registry_for_router(registry: ProxyRegistry) -> None:
    """Wire the ProxyRegistry into this router.

    Called once inside create_app() in server.py, using the same registry
    instance as registration_router.
    """
    global _registry
    _registry = registry


def _get_registry() -> ProxyRegistry:
    if _registry is None:
        raise HTTPException(status_code=500, detail="Proxy registry not initialized")
    return _registry


# ── public listing ────────────────────────────────────────────────────────────

@workspace_proxy_router.get(
    "/registry",
    summary="List all registered workspace tasks",
    include_in_schema=False,
)
async def list_registered() -> JSONResponse:
    """Return all tasks currently registered in the proxy (for debugging)."""
    return JSONResponse({"entries": _get_registry().list_all()})


# ── catch-all proxy ───────────────────────────────────────────────────────────

@workspace_proxy_router.api_route(
    "/{session_id}/{task_id}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    summary="Proxy workspace artifact request to the agent",
)
async def proxy_workspace(
    session_id: str,
    task_id: str,
    path: str,
    request: Request,
) -> Any:
    """Forward the request to the agent's WorkspaceServer.

    The agent_url is looked up from the ProxyRegistry. If the task is not
    registered (not yet created, or already deleted) the response is 404.
    """
    registry = _get_registry()
    agent_url = registry.lookup(session_id, task_id)

    if agent_url is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Workspace artifact not found: {session_id}/{task_id}. "
                "It may not have been created yet, or it has been deleted."
            ),
        )

    # Build upstream URL
    upstream = f"{agent_url}/{session_id}/{task_id}"
    if path:
        upstream += f"/{path}"
    else:
        upstream += "/"

    qs = request.url.query
    if qs:
        upstream += f"?{qs}"

    body = await request.body()
    fwd_headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }

    logger.debug(
        f"[workspace] proxy {request.method} "
        f"{session_id}/{task_id}/{path} → {upstream}"
    )

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
        logger.error(
            f"[workspace] agent unreachable for {session_id}/{task_id}: {agent_url}"
        )
        raise HTTPException(
            status_code=502,
            detail=(
                f"Agent workspace server is unreachable at {agent_url}. "
                "The agent may be down or restarting."
            ),
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Agent workspace server timed out.",
        )


# ── app root redirect ─────────────────────────────────────────────────────────
# Handle the case where the user hits /workspace/{session_id}/{task_id}
# without a trailing slash (would not match the :path route above).

@workspace_proxy_router.api_route(
    "/{session_id}/{task_id}",
    methods=["GET"],
    include_in_schema=False,
)
async def proxy_workspace_root(
    session_id: str,
    task_id: str,
    request: Request,
) -> Any:
    """Handle requests to the task root without a trailing slash."""
    return await proxy_workspace(
        session_id=session_id,
        task_id=task_id,
        path="",
        request=request,
    )
