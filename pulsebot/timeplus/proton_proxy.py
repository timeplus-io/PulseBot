"""Shared Proton HTTP streaming proxy helpers.

Both the WorkspaceServer (agent-side, port 8001) and the API server
(port 8000) expose a Proton SQL proxy.  This module holds the shared
streaming logic so neither duplicates it.

Protocol
--------
Client sends raw SQL as the POST body.
Server forwards it to Proton's HTTP interface (port 3218) and streams
the response back as NDJSON (application/x-ndjson).

This matches the protocol expected by @timeplus/proton-javascript-driver.
"""

from __future__ import annotations

import base64
import json
from typing import AsyncIterator

import httpx
from fastapi import Request
from fastapi.responses import StreamingResponse

from pulsebot.utils import get_logger

logger = get_logger(__name__)


def build_proton_headers(username: str = "", password: str = "") -> dict[str, str]:
    """Build HTTP headers for Proton requests, including Basic auth if credentials are set."""
    headers: dict[str, str] = {"Content-Type": "text/plain"}
    if username:
        creds = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers["Authorization"] = f"Basic {creds}"
    return headers


def build_proton_url(host: str = "localhost", port: int = 3218) -> str:
    """Build the Proton HTTP base URL."""
    return f"http://{host}:{port}"


async def stream_proton_query(
    sql: str,
    proton_url: str,
    headers: dict[str, str],
    fmt: str = "JSONEachRow",
) -> AsyncIterator[bytes]:
    """Async generator that forwards SQL to Proton and yields response bytes.

    Args:
        sql: Raw SQL query string.
        proton_url: Proton HTTP base URL (e.g. ``http://localhost:3218``).
        headers: HTTP headers including auth.
        fmt: Proton output format (default ``JSONEachRow`` for NDJSON).

    Yields:
        Raw response bytes from Proton.
    """
    target = f"{proton_url.rstrip('/')}/?default_format={fmt}"
    logger.debug("Proton proxy: sql=%r → %s", sql[:120], proton_url)

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                target,
                content=sql.encode(),
                headers=headers,
            ) as resp:
                if resp.status_code != 200:
                    error_body = await resp.aread()
                    logger.warning(
                        "Proton returned %d: %s",
                        resp.status_code,
                        error_body.decode()[:300],
                    )
                    yield error_body
                    return
                async for chunk in resp.aiter_bytes():
                    yield chunk
    except httpx.ConnectError as exc:
        logger.error("Proton unreachable at %s: %s", proton_url, exc)
        yield json.dumps({"error": f"Proton is unreachable at {proton_url}."}).encode()


async def make_proton_streaming_response(
    request: Request,
    proton_url: str,
    headers: dict[str, str],
) -> StreamingResponse:
    """Parse the request body as SQL and return a StreamingResponse from Proton.

    Args:
        request: Incoming FastAPI request (body must be raw SQL).
        proton_url: Proton HTTP base URL.
        headers: HTTP headers including auth.

    Returns:
        StreamingResponse with NDJSON content from Proton.

    Raises:
        fastapi.HTTPException: If the request body is empty.
    """
    from fastapi import HTTPException

    body = await request.body()
    sql = body.decode(errors="replace").strip()

    if not sql:
        raise HTTPException(status_code=400, detail="Request body must be a SQL query string.")

    fmt = request.query_params.get("default_format", "JSONEachRow")

    return StreamingResponse(
        content=stream_proton_query(sql, proton_url, headers, fmt),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
