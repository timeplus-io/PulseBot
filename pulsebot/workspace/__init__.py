"""Agent Workspace package.

Agent side imports:
  WorkspaceConfig         Pydantic config model
  WorkspaceManager        Directory + subprocess management
  run_workspace_server    Start the embedded HTTP server (asyncio task)
  ProxyRegistryClient     Registers tasks with the API server

API server side imports:
  WorkspaceConfig         Pydantic config model (for internal_api_key)
  ProxyRegistry           In-memory session/task → agent_url map
  workspace_proxy_router  FastAPI router: ANY /workspace/{s}/{t}/{path}
  registration_router     FastAPI router: /internal/workspace/register
  set_proxy_registry_for_router   wire ProxyRegistry into proxy router
  set_proxy_registry              wire ProxyRegistry into registration router
"""

from pulsebot.workspace.config import WorkspaceConfig
from pulsebot.workspace.manager import WorkspaceManager
from pulsebot.workspace.proxy_registry import ProxyRegistry
from pulsebot.workspace.proxy_router import (
    workspace_proxy_router,
    set_proxy_registry_for_router,
)
from pulsebot.workspace.registration_router import (
    registration_router,
    set_proxy_registry,
)
from pulsebot.workspace.registry_client import ProxyRegistryClient
from pulsebot.workspace.server import run_workspace_server

__all__ = [
    # shared
    "WorkspaceConfig",
    # agent side
    "WorkspaceManager",
    "ProxyRegistryClient",
    "run_workspace_server",
    # API server side
    "ProxyRegistry",
    "workspace_proxy_router",
    "registration_router",
    "set_proxy_registry_for_router",
    "set_proxy_registry",
]
