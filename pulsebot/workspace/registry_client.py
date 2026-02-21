"""ProxyRegistryClient — agent-side HTTP client for workspace registration.

The agent calls the API server's /internal/workspace/register endpoint
after creating an artifact, to expose a public proxy route for it.
This is the only HTTP call the agent ever makes to the API server for workspace.

Usage::

    client = ProxyRegistryClient(cfg)
    result = await client.register(
        session_id="abc-123",
        task_id="cpu-monitor",
        artifact_type="fullstack_app",
    )
    public_url = result["public_url"]

    # On delete:
    await client.deregister("abc-123", "cpu-monitor")
"""

from __future__ import annotations

import os
import httpx

from pulsebot.utils import get_logger
from pulsebot.workspace.config import WorkspaceConfig

logger = get_logger(__name__)


class ProxyRegistryClient:
    """Registers and deregisters workspace tasks with the API server.

    Args:
        config: WorkspaceConfig (uses api_server_url, internal_api_key, agent_base_url).
    """

    def __init__(self, config: WorkspaceConfig) -> None:
        self._cfg = config

    @property
    def _headers(self) -> dict[str, str]:
        return {"X-Internal-Key": self._cfg.internal_api_key}

    async def register(
        self,
        session_id: str,
        task_id: str,
        artifact_type: str,
    ) -> dict:
        """Register a task with the API server proxy registry.

        Args:
            session_id: Conversation session ID.
            task_id: Task slug.
            artifact_type: One of "file", "html_app", "fullstack_app".

        Returns:
            Dict containing at minimum ``public_url``.

        Raises:
            httpx.HTTPStatusError: API server returned a non-2xx response.
            httpx.ConnectError: API server is not reachable.
        """
        url = f"{self._cfg.api_server_url}/internal/workspace/register"

        # Read directly from env — bypasses pydantic nested model issue entirely
        agent_host = os.environ.get("AGENT_HOST") or self._cfg.agent_host
        agent_port = os.environ.get("WORKSPACE_PORT") or str(self._cfg.workspace_port)
        agent_url = f"http://{agent_host}:{agent_port}"
        
        logger.info(f"[workspace] registering session={session_id} task={task_id} agent_url={agent_url}")
        
        payload = {
            "session_id": session_id,
            "task_id": task_id,
            "agent_url": agent_url,
            "artifact_type": artifact_type,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload, headers=self._headers)

        resp.raise_for_status()
        data = resp.json()

        logger.info(
            f"[workspace] registered session={session_id} task={task_id} "
            f"public_url={data.get('public_url')}"
        )
        return data

    async def deregister(self, session_id: str, task_id: str) -> None:
        """Remove a task registration from the API server proxy registry.

        Args:
            session_id: Conversation session ID.
            task_id: Task slug.
        """
        url = (
            f"{self._cfg.api_server_url}/internal/workspace/register"
            f"/{session_id}/{task_id}"
        )

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.delete(url, headers=self._headers)

        if resp.status_code == 404:
            logger.debug(
                f"[workspace] deregister: {session_id}/{task_id} was not registered"
            )
            return

        resp.raise_for_status()
        logger.info(f"[workspace] deregistered session={session_id} task={task_id}")
