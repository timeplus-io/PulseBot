"""FastAPI server for PulseBot webchat and management API."""

from __future__ import annotations

import json
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from pulsebot.config import Config, load_config
from pulsebot.timeplus.proton_proxy import (
    build_proton_headers,
    build_proton_url,
    make_proton_streaming_response,
)
from pulsebot.timeplus.streams import StreamReader, StreamWriter
from pulsebot.utils import get_logger

from pulsebot.workspace import (
    ProxyRegistry,
    workspace_proxy_router,
    registration_router,
    set_proxy_registry,
    set_proxy_registry_for_router,
)

logger = get_logger(__name__)

# Global state
_config: Config | None = None
_config_path: str = "config.yaml"
_writer: StreamWriter | None = None
_reader: StreamReader | None = None
_tp_client = None  # TimeplusClient, typed as Any to avoid circular import

_proxy_registry: ProxyRegistry | None = None


# Sensitive field names whose values should be masked in GET /config responses
_SENSITIVE_FIELDS = {"api_key", "password", "token", "auth_token", "internal_api_key"}


def _mask_secrets(obj: Any) -> Any:
    """Recursively mask sensitive fields in a config dict."""
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                result[k] = _mask_secrets(v)
            elif k in _SENSITIVE_FIELDS and v:
                result[k] = "***"
            else:
                result[k] = v
        return result
    if isinstance(obj, list):
        return [_mask_secrets(i) for i in obj]
    return obj


def _deep_merge(base: dict, overlay: dict) -> dict:
    """Recursively merge overlay into base, returning a new dict."""
    result = dict(base)
    for k, v in overlay.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _classify_db_error(exc: Exception) -> str:
    """Return a human-readable message for a database write/connect failure.

    Matches well-known Proton/ClickHouse error codes for a specific hint;
    falls back to the raw exception message for everything else so that no
    error is silently swallowed or misrepresented.
    """
    msg = str(exc)
    if "max_disk_util" in msg or "2529" in msg:
        return "Database disk is full. The agent cannot respond until disk space is freed."
    if "Connection refused" in msg or "ConnectionRefused" in msg:
        return "Cannot connect to the database. Check that Proton/Timeplus is running."
    if "Authentication failed" in msg or "194" in msg:
        return "Database authentication failed. Check credentials in config.yaml."
    if "Code:" in msg:
        # Generic Proton exception — include the code for actionability
        return f"Database error: {msg}"
    # Network / OS / unknown
    return f"Unexpected error communicating with the database: {msg}"


class ChatRequest(BaseModel):
    """Chat message request."""
    message: str = Field(..., description="The content of the chat message to send to the agent.")
    session_id: str | None = Field(default=None, description="Optional UUID session ID. If not provided, a new one is generated.")


class ChatResponse(BaseModel):
    """Chat message response."""
    session_id: str = Field(..., description="The session ID associated with this chat.")
    message_id: str = Field(..., description="The unique ID of the stored message in Timeplus.")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status (e.g., 'ok').")
    version: str = Field(..., description="Current API version.")


class TaskTriggerRequest(BaseModel):
    """Incoming callback from a Timeplus Python UDF."""
    task_id: str = Field(..., description="The ID of the task being triggered.")
    task_name: str = Field(..., description="The human-readable name of the task.")
    prompt: str = Field(..., description="The LLM prompt instructing the agent what to do for this task.")
    trigger_type: str = Field(default="interval", description="Type of trigger, either 'interval' or 'cron'.")
    cron_expression: str | None = Field(default=None, description="The cron expression if the trigger type is cron.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the task execution.")


class TaskTriggerResponse(BaseModel):
    """Response to the Timeplus Python UDF callback."""
    execution_id: str = Field(..., description="The unique identifier for this task execution.")
    session_id: str = Field(..., description="The global session ID used for this scheduled task.")
    status: str = Field(default="triggered", description="The status of the trigger request.")


class ProjectTriggerRequest(BaseModel):
    """Request body for triggering a scheduled project run."""
    trigger_prompt: str | None = Field(
        default=None,
        description="Prompt to send to worker agents. Falls back to the project's default trigger_prompt if omitted.",
    )


class ProjectTriggerResponse(BaseModel):
    """Response for a project trigger request."""
    project_id: str = Field(..., description="The project that was triggered.")
    status: str = Field(default="triggered", description="Trigger status.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global _config, _config_path, _writer, _reader, _tp_client, _proxy_registry

    # Startup
    logger.info("Starting PulseBot API server")

    try:
        from pulsebot.timeplus.client import TimeplusClient

        _config = load_config(_config_path)

        _proxy_registry = ProxyRegistry()
        internal_key = _config.workspace.internal_api_key
        set_proxy_registry(_proxy_registry, internal_key)
        set_proxy_registry_for_router(_proxy_registry)
        logger.info("Workspace proxy registry initialized")

        client = TimeplusClient.from_config(_config.timeplus)
        _tp_client = client

        from pulsebot.timeplus.setup import create_streams
        await create_streams(client)

        _writer = StreamWriter(client, "messages")
        _reader = StreamReader(client, "messages")

        logger.info("API server initialized")
    except Exception as e:
        logger.error(f"Failed to initialize API server: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down API server")


def create_app(config: Config | None = None, config_path: str = "config.yaml") -> FastAPI:
    """Create FastAPI application.

    Args:
        config: Optional configuration override
        config_path: Path to config.yaml used for reads/writes via the config API

    Returns:
        Configured FastAPI app
    """
    global _config, _config_path
    _config_path = config_path
    
    if config:
        _config = config
    
    app = FastAPI(
        title="PulseBot API",
        description="Stream-native AI agent API",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # Add CORS middleware — origins controlled by config.api.cors_origins
    cors_origins = _config.api.cors_origins if _config else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include router
    app.include_router(router)
    
    app.include_router(workspace_proxy_router, tags=["Workspace Proxy"])
    app.include_router(registration_router, tags=["Workspace Registration"])

    # Serve web UI static files
    web_dir = Path(__file__).parent.parent / "web"
    if web_dir.exists():
        app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")

    return app


# API Router
from fastapi import APIRouter

router = APIRouter()


@router.get("/", include_in_schema=False)
async def serve_web_ui() -> FileResponse:
    """Serve the web chat UI."""
    web_dir = Path(__file__).parent.parent / "web"
    index_path = web_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    raise HTTPException(status_code=404, detail="Web UI not found")


@router.get("/config", tags=["System"])
async def get_config() -> dict[str, Any]:
    """Return the current configuration with secrets masked.

    API keys, passwords, and tokens are replaced with ``"***"`` when non-empty.
    """
    if _config is None:
        raise HTTPException(status_code=500, detail="Server not initialized")
    raw = _config.model_dump()
    return _mask_secrets(raw)


@router.patch("/config", tags=["System"])
async def update_config(updates: dict[str, Any]) -> dict[str, Any]:
    """Deep-merge partial updates into the running configuration and persist to disk.

    Only the fields present in the request body are changed — omitted fields
    keep their current values.  Secrets are masked in the response.

    Changes take effect immediately for new agent interactions.  Some settings
    (e.g. channels, Timeplus connection) require a server restart to fully
    apply.

    Example body to change just the active model::

        {"agent": {"model": "gpt-4o", "provider": "openai"}}
    """
    global _config
    if _config is None:
        raise HTTPException(status_code=500, detail="Server not initialized")

    # Deep-merge updates onto current config dict
    current = _config.model_dump()
    merged = _deep_merge(current, updates)

    try:
        _config = Config(**merged)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid config: {e}") from e

    # Persist to config.yaml — best-effort; in-memory update always succeeds.
    persist_warning: str | None = None
    try:
        import yaml as _yaml
        config_file = Path(_config_path)
        if config_file.exists():
            with open(config_file) as f:
                existing_yaml = _yaml.safe_load(f) or {}
            saved = _deep_merge(existing_yaml, updates)
        else:
            saved = merged
        with open(config_file, "w") as f:
            _yaml.dump(saved, f, default_flow_style=False, allow_unicode=True)
        logger.info("Configuration updated and persisted via API", extra={"keys": list(updates.keys())})
    except OSError as e:
        persist_warning = f"Settings applied in memory but could not be saved to disk: {e}"
        logger.warning("Config persist failed (read-only fs?): %s", e)
    except Exception as e:
        persist_warning = f"Settings applied in memory but file write failed: {e}"
        logger.warning("Config persist error: %s", e)

    result = _mask_secrets(_config.model_dump())
    if persist_warning:
        result["_warning"] = persist_warning
    return result


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok", version="0.1.0")


@router.post("/query", tags=["Query"])
async def proton_query(request: Request) -> StreamingResponse:
    """Proxy raw SQL to Proton and stream NDJSON results back.

    Accepts a raw SQL string as the request body.
    Results are streamed as NDJSON (one JSON object per line).

    Compatible with ``@timeplus/proton-javascript-driver`` — point the driver
    at ``http://<api-host>:<port>/query`` instead of connecting directly to Proton.

    Query parameters:
    - ``default_format``: Proton output format (default ``JSONEachRow``).

    Example::

        const resp = await fetch('http://localhost:8000/query', {
          method: 'POST',
          body: 'SELECT * FROM pulsebot.events LIMIT 10',
        });
        for await (const line of resp.body) { console.log(JSON.parse(line)); }
    """
    if _config is None:
        raise HTTPException(status_code=500, detail="Server not initialized")

    proton_url = build_proton_url(
        host=_config.timeplus.host,
        port=3218,
    )
    headers = build_proton_headers(
        username=_config.timeplus.username,
        password=_config.timeplus.password,
    )
    return await make_proton_streaming_response(request, proton_url, headers)


@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def send_chat_message(request: ChatRequest) -> ChatResponse:
    """Send a chat message to the agent.
    
    Returns immediately with session/message IDs.
    Use WebSocket or SSE for real-time responses.
    """
    if _writer is None:
        raise HTTPException(status_code=500, detail="Server not initialized")
    
    session_id = request.session_id or str(uuid.uuid4())
    
    message_id = await _writer.write({
        "source": "webchat",
        "target": "agent",
        "session_id": session_id,
        "message_type": "user_input",
        "content": json.dumps({"text": request.message}),
        "user_id": "",
        "priority": 0,
    })
    
    logger.info(
        "Chat message received",
        extra={"session_id": session_id, "message_id": message_id}
    )
    
    return ChatResponse(session_id=session_id, message_id=message_id)


@router.post("/api/v1/task-trigger", response_model=TaskTriggerResponse, tags=["Tasks"])
async def trigger_task(request: TaskTriggerRequest) -> TaskTriggerResponse:
    """Receive a scheduled task callback from a Timeplus Python UDF.

    Writes a 'scheduled_task' message into the messages stream so the
    agent loop processes it under the task's global session.
    """
    if _writer is None:
        raise HTTPException(status_code=500, detail="Server not initialized")

    session_id = f"global_task_{request.task_name}"

    execution_id = await _writer.write({
        "source": "scheduler",
        "target": "agent",
        "session_id": session_id,
        "message_type": "scheduled_task",
        "content": json.dumps({
            "text": request.prompt,
            "task_id": request.task_id,
            "task_name": request.task_name,
            "trigger_type": request.trigger_type,
        }),
        "user_id": "system",
        "priority": 1,
    })

    logger.info(
        "Task trigger received",
        extra={"task_name": request.task_name, "session_id": session_id},
    )

    return TaskTriggerResponse(
        execution_id=execution_id,
        session_id=session_id,
    )


@router.post(
    "/api/v1/projects/{project_id}/trigger",
    response_model=ProjectTriggerResponse,
    tags=["Projects"],
)
async def trigger_project(project_id: str, request: ProjectTriggerRequest) -> ProjectTriggerResponse:
    """Trigger one scheduled execution of a multi-agent project.

    Called by the Timeplus Python UDF on each schedule tick. The endpoint
    writes a 'trigger' kanban message for the ManagerAgent to pick up.
    Returns 404 if the project does not exist or is not active.

    The ManagerAgent handles skip-if-busy internally: if a run is already
    in progress when the trigger arrives, it logs a warning and discards it.
    """
    if _tp_client is None or _config is None:
        raise HTTPException(status_code=500, detail="Server not initialized")

    # Verify the project exists and is an active scheduled project.
    from pulsebot.timeplus.client import escape_sql_str

    check_sql = f"""
    SELECT project_id, session_id, is_scheduled, trigger_prompt
    FROM table(pulsebot.kanban_projects)
    WHERE project_id = '{escape_sql_str(project_id)}'
    ORDER BY timestamp DESC
    LIMIT 1
    """
    rows = _tp_client.query(check_sql)
    if not rows:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

    row = rows[0]
    if not row.get("is_scheduled"):
        raise HTTPException(status_code=400, detail=f"Project {project_id} is not a scheduled project")

    # Use provided prompt or fall back to the stored default.
    prompt = request.trigger_prompt or row.get("trigger_prompt", "")

    # Write the trigger message to the kanban stream.
    import json as _json
    _tp_client.insert("pulsebot.kanban", [{
        "project_id": project_id,
        "sender_id": "scheduler",
        "target_id": f"manager_{project_id}",
        "msg_type": "trigger",
        "content": _json.dumps({"prompt": prompt}),
    }])

    logger.info(
        "Project trigger written to kanban",
        extra={"project_id": project_id},
    )
    return ProjectTriggerResponse(project_id=project_id)


@router.websocket("/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str) -> None:
    """WebSocket endpoint for real-time chat.
    
    Messages from client: {"type": "message", "text": "..."}
    Messages from server: {"type": "response", "text": "..."}
    """
    await websocket.accept()
    
    if _writer is None or _config is None:
        await websocket.close(code=1011, reason="Server not initialized")
        return
    
    import asyncio
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.streams import StreamReader
    
    # Create dedicated client for this WebSocket to avoid simultaneous query issues
    ws_client = TimeplusClient.from_config(_config.timeplus)
    ws_reader = StreamReader(ws_client, "messages")
    
    logger.info(f"WebSocket connected: {session_id}")

    
    async def receive_messages():
        """Handle incoming WebSocket messages."""
        try:
            while True:
                data = await websocket.receive_json()

                if data.get("type") == "message":
                    text = data.get("text", "")
                    try:
                        await _writer.write({
                            "source": "webchat",
                            "target": "agent",
                            "session_id": session_id,
                            "message_type": "user_input",
                            "content": json.dumps({"text": text}),
                            "priority": 0,
                        })
                    except Exception as write_exc:
                        logger.error(f"WebSocket message write failed: {write_exc}")
                        try:
                            await websocket.send_json({
                                "type": "system_error",
                                "message": _classify_db_error(write_exc),
                            })
                        except Exception:
                            pass

        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {session_id}")
        except Exception as e:
            logger.error(f"WebSocket receive error: {e}")
    
    async def send_responses():
        """Send agent responses and tool calls to WebSocket."""
        query = f"""
            SELECT * FROM pulsebot.messages
            WHERE session_id = '{session_id}'
              AND target = 'channel:webchat'
              AND message_type IN ('agent_response', 'tool_call', 'llm_thinking')
            SETTINGS seek_to='latest'
        """

        logger.info(f"Starting send_responses stream for session: {session_id}")

        try:
            async for message in ws_reader.stream(query):
                # Check if websocket is still connected
                if websocket.client_state.name != "CONNECTED":
                    logger.info(f"WebSocket no longer connected, stopping stream: {session_id}")
                    break

                message_type = message.get("message_type", "")
                content_str = message.get("content", "{}")

                try:
                    content = json.loads(content_str)
                except json.JSONDecodeError:
                    content = {"text": content_str}

                try:
                    if message_type == "tool_call":
                        # Send tool call event
                        await websocket.send_json({
                            "type": "tool_call",
                            "tool_name": content.get("tool_name", ""),
                            "status": content.get("status", ""),
                            "arguments": content.get("arguments", {}),
                            "args_summary": content.get("args_summary", ""),
                            "result_preview": content.get("result_preview", ""),
                            "duration_ms": content.get("duration_ms", 0),
                            "message_id": message.get("id", ""),
                        })
                        logger.debug(f"Sent tool_call to WebSocket: {content.get('tool_name')}")
                    elif message_type == "llm_thinking":
                        # Send LLM thinking event
                        await websocket.send_json({
                            "type": "llm_thinking",
                            "status": content.get("status", ""),
                            "iteration": content.get("iteration", 1),
                            "duration_ms": content.get("duration_ms", 0),
                            "message_id": message.get("id", ""),
                        })
                        logger.debug(f"Sent llm_thinking to WebSocket: iteration={content.get('iteration')} status={content.get('status')}")
                    else:
                        # Send regular response
                        text = content.get("text", "")
                        logger.info(f"Sending response to WebSocket: {session_id}, text length: {len(text)}")
                        await websocket.send_json({
                            "type": "response",
                            "text": text,
                            "message_id": message.get("id", ""),
                        })
                except RuntimeError as e:
                    # WebSocket closed while sending
                    logger.info(f"WebSocket closed during send: {session_id}")
                    break

        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected during send_responses: {session_id}")
        except Exception as e:
            logger.error(f"WebSocket send error: {e}", exc_info=True)
        finally:
            logger.info(f"send_responses ended for session: {session_id}")
    
    async def forward_task_notifications():
        """Forward task_notification and agent error events to this WebSocket client."""
        ws_events_client = TimeplusClient.from_config(_config.timeplus)
        ws_events_reader = StreamReader(ws_events_client, "events")

        events_query = """
            SELECT * FROM pulsebot.events
            WHERE event_type IN ('task_notification', 'llm.call_failed', 'session.error')
            SETTINGS seek_to='latest'
        """
        try:
            async for event in ws_events_reader.stream(events_query):
                if websocket.client_state.name != "CONNECTED":
                    break
                try:
                    event_type = event.get("event_type", "")
                    payload = json.loads(event.get("payload", "{}"))
                    if event_type == "task_notification":
                        text = payload.get("text", "")
                        if not text:
                            continue
                        await websocket.send_json({
                            "type": "task_notification",
                            "task_name": payload.get("task_name", ""),
                            "text": text,
                        })
                    elif event_type in ("llm.call_failed", "session.error"):
                        # Safety net: if the agent_response message was missed or
                        # failed to write, forward the error event directly so the
                        # UI can unblock and show the error.
                        if payload.get("session_id") != session_id:
                            continue
                        error = payload.get("error", "An error occurred while processing your request")
                        await websocket.send_json({
                            "type": "system_error",
                            "message": error,
                        })
                except RuntimeError:
                    break
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected during task notifications: {session_id}")
        except Exception as e:
            logger.error(f"WebSocket task_notification stream error: {e}")

    async def forward_agent_status():
        """Forward agent.ready events so the UI can gate message sending.

        Seeks back 10 minutes to catch agents already running when the client
        connects. Sends {"type": "agent_ready"} to the UI on each agent.ready
        event (covers restarts too).
        """
        import datetime as _dt
        ws_status_client = TimeplusClient.from_config(_config.timeplus)
        ws_status_reader = StreamReader(ws_status_client, "events")

        seek_back = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        status_query = f"""
            SELECT * FROM pulsebot.events
            WHERE event_type = 'agent.ready'
            SETTINGS seek_to='{seek_back}'
        """
        try:
            async for _event in ws_status_reader.stream(status_query):
                if websocket.client_state.name != "CONNECTED":
                    break
                try:
                    await websocket.send_json({"type": "agent_ready"})
                except RuntimeError:
                    break
        except WebSocketDisconnect:
            pass
        except Exception as e:
            logger.error(f"WebSocket agent_status stream error: {e}")

    async def monitor_system_health():
        """Periodically check Proton write availability and notify the UI on failure.

        Attempts a lightweight insert every 30 seconds. If it fails with a
        disk-full or other write error, sends a ``system_error`` event directly
        to the WebSocket client so the UI can surface the issue without waiting
        for a user message attempt or an agent response timeout.
        """
        import datetime as _dt
        _last_error: str | None = None
        while True:
            await asyncio.sleep(30)
            if websocket.client_state.name != "CONNECTED":
                break
            try:
                ws_health_client = TimeplusClient.from_config(_config.timeplus)
                ws_health_client.insert("pulsebot.events", [{
                    "event_type": "system.health_check",
                    "source": "api:health",
                    "severity": "debug",
                    "payload": "{}",
                    "tags": ["system"],
                    "id": "health-check",
                    "timestamp": _dt.datetime.now(_dt.timezone.utc),
                }])
                # Write succeeded — clear any previous error state
                if _last_error is not None:
                    _last_error = None
                    try:
                        await websocket.send_json({
                            "type": "system_info",
                            "message": "Database is back online. You can send messages again.",
                        })
                    except Exception:
                        pass
            except Exception as health_exc:
                msg = _classify_db_error(health_exc)
                # Only send the error once per continuous failure run (avoid flooding)
                if msg != _last_error:
                    _last_error = msg
                    logger.warning(f"System health check failed: {health_exc}")
                    try:
                        await websocket.send_json({"type": "system_error", "message": msg})
                    except Exception:
                        break

    # Run all tasks concurrently.
    # Only receive_messages() signals client disconnect — when it finishes,
    # cancel the background stream tasks. Background tasks failing on their own
    # (e.g. Proton hiccup) must NOT kill the WebSocket and miss queued results.
    receive_task = asyncio.create_task(receive_messages())
    send_task = asyncio.create_task(send_responses())
    notify_task = asyncio.create_task(forward_task_notifications())
    agent_status_task = asyncio.create_task(forward_agent_status())
    health_task = asyncio.create_task(monitor_system_health())

    try:
        await receive_task
    except Exception as e:
        logger.error(f"WebSocket receive_task error: {e}")
    finally:
        for task in (send_task, notify_task, agent_status_task, health_task):
            task.cancel()
        await asyncio.gather(send_task, notify_task, agent_status_task, health_task, return_exceptions=True)


@router.get("/sessions/{session_id}/history", tags=["Chat"])
async def get_session_history(session_id: str, limit: int = 50) -> list[dict[str, Any]]:
    """Get conversation history for a session."""
    if _reader is None:
        raise HTTPException(status_code=500, detail="Server not initialized")
    
    messages = _reader.read_history(session_id=session_id, limit=limit)
    
    return [
        {
            "id": m.get("id"),
            "timestamp": str(m.get("timestamp")),
            "type": m.get("message_type"),
            "content": m.get("content"),
            "source": m.get("source"),
        }
        for m in messages
    ]
