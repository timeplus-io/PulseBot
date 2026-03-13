"""WebhookHook — POST tool call info to an external HTTP endpoint."""

from __future__ import annotations

from typing import Any

import httpx

from pulsebot.hooks.base import HookVerdict, ToolCallHook
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class WebhookHook(ToolCallHook):
    """Sends pre-call information to an external HTTP endpoint.

    The endpoint should respond with JSON:
    ``{"verdict": "approve"|"deny"|"modify", "reasoning": "...",
    "modified_arguments": {...}}``.

    Args:
        url: HTTP/HTTPS endpoint to POST to.
        auth_header: Optional ``Authorization`` header value.
        timeout: Request timeout in seconds (default 5.0).
        fail_open: If True (default), approve on network/timeout errors.
            If False, deny on errors (fail-closed / stricter).
    """

    def __init__(
        self,
        url: str,
        auth_header: str | None = None,
        timeout: float = 5.0,
        fail_open: bool = True,
    ) -> None:
        self._url = url
        self._headers: dict[str, str] = {"Content-Type": "application/json"}
        if auth_header:
            self._headers["Authorization"] = auth_header
        self._timeout = timeout
        self._fail_open = fail_open

    async def pre_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> HookVerdict:
        """POST the tool call to the webhook; return the endpoint's verdict."""
        payload = {
            "tool_name": tool_name,
            "arguments": arguments,
            "session_id": session_id,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._url,
                    json=payload,
                    headers=self._headers,
                    timeout=self._timeout,
                )
                data = response.json()
                verdict = data.get("verdict", "approve")
                if verdict not in ("approve", "deny", "modify"):
                    verdict = "approve"
                # "modify" requires modified_arguments — fall back to approve if missing
                if verdict == "modify" and not data.get("modified_arguments"):
                    verdict = "approve"
                return HookVerdict(
                    verdict=verdict,
                    reasoning=data.get("reasoning"),
                    modified_arguments=data.get("modified_arguments") if verdict == "modify" else None,
                )
        except Exception as exc:
            logger.warning(
                "WebhookHook pre_call failed",
                extra={"url": self._url, "error": str(exc)},
            )
            if self._fail_open:
                return HookVerdict(verdict="approve", reasoning=f"Webhook error (fail-open): {exc}")
            return HookVerdict(verdict="deny", reasoning=f"Webhook error (fail-closed): {exc}")

    async def post_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
        session_id: str = "",
    ) -> None:
        """POST the tool result to the webhook for observability (fire-and-forget)."""
        payload = {
            "event": "post_call",
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "session_id": session_id,
        }
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    self._url,
                    json=payload,
                    headers=self._headers,
                    timeout=self._timeout,
                )
        except Exception as exc:
            logger.warning(
                "WebhookHook post_call failed",
                extra={"url": self._url, "error": str(exc)},
            )
