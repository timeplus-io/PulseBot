"""RegistrationRouter — API server internal endpoints for workspace registration.

Endpoints (all protected by X-Internal-Key):
  POST   /internal/workspace/register
  DELETE /internal/workspace/register/{session_id}/{task_id}
  GET    /internal/workspace/registry      (debug listing)

Called exclusively by the agent's ProxyRegistryClient. Never by end users.
Wired into the FastAPI app in server.py.
"""

from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from pulsebot.utils import get_logger
from pulsebot.workspace.proxy_registry import ProxyRegistry

logger = get_logger(__name__)

registration_router = APIRouter(prefix="/internal/workspace", tags=["workspace-internal"])

# Injected once from server.py via set_proxy_registry()
_registry: ProxyRegistry | None = None
_internal_api_key: str = ""


def set_proxy_registry(registry: ProxyRegistry, internal_api_key: str) -> None:
    """Wire the ProxyRegistry and shared secret into this router.

    Called once inside create_app() in server.py.
    """
    global _registry, _internal_api_key
    _registry = registry
    _internal_api_key = internal_api_key


def _get_registry() -> ProxyRegistry:
    if _registry is None:
        raise HTTPException(status_code=500, detail="Proxy registry not initialized")
    return _registry


# ── auth guard ────────────────────────────────────────────────────────────────

def _require_internal_key(x_internal_key: str = Header(default="")) -> None:
    """FastAPI dependency: reject requests without the correct shared secret."""
    if not _internal_api_key:
        raise HTTPException(
            status_code=403,
            detail="Internal workspace endpoints are disabled (no internal_api_key configured).",
        )
    if not secrets.compare_digest(_internal_api_key, x_internal_key):
        raise HTTPException(status_code=403, detail="Invalid X-Internal-Key")


# ── request model ─────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    session_id: str
    task_id: str
    agent_url: str
    artifact_type: str   # "file" | "html_app" | "fullstack_app"


# ── endpoints ─────────────────────────────────────────────────────────────────

@registration_router.post(
    "/register",
    summary="[Internal] Register a workspace task",
    dependencies=[Depends(_require_internal_key)],
)
async def register_task(body: RegisterRequest) -> JSONResponse:
    """Register a workspace task so the proxy router can forward requests to it.

    Called by the agent after creating an artifact and making it ready to serve.
    Returns the public URL the user should be given.
    """
    registry = _get_registry()

    await registry.register(
        session_id=body.session_id,
        task_id=body.task_id,
        agent_url=body.agent_url,
        artifact_type=body.artifact_type,
    )

    # Build the public URL the agent will share with the user
    # We reconstruct it from the request so the router doesn't need to know
    # the API server's own public base_url — the agent passes agent_url and
    # the public URL is simply the proxy path on this server.
    # The agent already knows base_url from its config; we echo it back
    # derived from the request's Host header or just the path.
    public_path = f"/workspace/{body.session_id}/{body.task_id}/"

    logger.info(
        f"[workspace] registered session={body.session_id} task={body.task_id} "
        f"agent_url={body.agent_url} type={body.artifact_type}"
    )

    return JSONResponse({
        "status": "registered",
        "session_id": body.session_id,
        "task_id": body.task_id,
        "public_path": public_path,
    })


@registration_router.delete(
    "/register/{session_id}/{task_id}",
    summary="[Internal] Deregister a workspace task",
    dependencies=[Depends(_require_internal_key)],
)
async def deregister_task(session_id: str, task_id: str) -> JSONResponse:
    """Remove a task from the proxy registry.

    Called by the agent when a task is deleted. After this the proxy router
    returns 404 for that task's public URLs.
    """
    registry = _get_registry()
    existed = await registry.deregister(session_id, task_id)

    logger.info(
        f"[workspace] deregistered session={session_id} task={task_id} "
        f"existed={existed}"
    )

    return JSONResponse({
        "status": "deregistered",
        "session_id": session_id,
        "task_id": task_id,
    })


@registration_router.get(
    "/registry",
    summary="[Internal] List all registered tasks",
    dependencies=[Depends(_require_internal_key)],
)
async def list_registry() -> JSONResponse:
    """Return all currently registered workspace tasks (for debugging)."""
    registry = _get_registry()
    return JSONResponse({"entries": registry.list_all()})
