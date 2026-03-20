"""FastAPI server for PulseBot webchat and management API."""

from __future__ import annotations

import json
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from pulsebot.config import Config, load_config
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
_writer: StreamWriter | None = None
_reader: StreamReader | None = None

_proxy_registry: ProxyRegistry | None = None


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global _config, _writer, _reader, _proxy_registry
    
    # Startup
    logger.info("Starting PulseBot API server")
    
    try:
        from pulsebot.timeplus.client import TimeplusClient
        
        _config = load_config()
        
        _proxy_registry = ProxyRegistry()
        internal_key = _config.workspace.internal_api_key
        set_proxy_registry(_proxy_registry, internal_key)
        set_proxy_registry_for_router(_proxy_registry)
        logger.info("Workspace proxy registry initialized")
        
        client = TimeplusClient.from_config(_config.timeplus)
        
        _writer = StreamWriter(client, "messages")
        _reader = StreamReader(client, "messages")
        
        logger.info("API server initialized")
    except Exception as e:
        logger.error(f"Failed to initialize API server: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down API server")


def create_app(config: Config | None = None) -> FastAPI:
    """Create FastAPI application.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Configured FastAPI app
    """
    global _config
    
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


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok", version="0.1.0")


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
                    
                    await _writer.write({
                        "source": "webchat",
                        "target": "agent",
                        "session_id": session_id,
                        "message_type": "user_input",
                        "content": json.dumps({"text": text}),
                        "priority": 0,
                    })
                    
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
        """Forward task_notification events to this WebSocket client."""
        ws_events_client = TimeplusClient.from_config(_config.timeplus)
        ws_events_reader = StreamReader(ws_events_client, "events")

        events_query = """
            SELECT * FROM pulsebot.events
            WHERE event_type = 'task_notification'
            SETTINGS seek_to='latest'
        """
        try:
            async for event in ws_events_reader.stream(events_query):
                if websocket.client_state.name != "CONNECTED":
                    break
                try:
                    payload = json.loads(event.get("payload", "{}"))
                    text = payload.get("text", "")
                    if not text:
                        continue
                    await websocket.send_json({
                        "type": "task_notification",
                        "task_name": payload.get("task_name", ""),
                        "text": text,
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

    # Run all tasks concurrently
    receive_task = asyncio.create_task(receive_messages())
    send_task = asyncio.create_task(send_responses())
    notify_task = asyncio.create_task(forward_task_notifications())
    agent_status_task = asyncio.create_task(forward_agent_status())

    try:
        done, pending = await asyncio.wait(
            {receive_task, send_task, notify_task, agent_status_task},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
    except Exception:
        receive_task.cancel()
        send_task.cancel()
        notify_task.cancel()
        agent_status_task.cancel()


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
