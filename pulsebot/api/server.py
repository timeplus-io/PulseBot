"""FastAPI server for PulseBot webchat and management API."""

from __future__ import annotations

import json
import uuid
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pulsebot.config import Config, load_config
from pulsebot.timeplus.streams import StreamReader, StreamWriter
from pulsebot.utils import get_logger

logger = get_logger(__name__)

# Global state
_config: Config | None = None
_writer: StreamWriter | None = None
_reader: StreamReader | None = None


class ChatRequest(BaseModel):
    """Chat message request."""
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    """Chat message response."""
    session_id: str
    message_id: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global _config, _writer, _reader
    
    # Startup
    logger.info("Starting PulseBot API server")
    
    try:
        from pulsebot.timeplus.client import TimeplusClient
        
        _config = load_config()
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
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include router
    app.include_router(router)
    
    return app


# API Router
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok", version="0.1.0")


@router.post("/chat", response_model=ChatResponse)
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
        """Send agent responses to WebSocket."""
        query = f"""
            SELECT * FROM messages 
            WHERE session_id = '{session_id}'
              AND target = 'channel:webchat'
              AND message_type = 'agent_response'
            SETTINGS seek_to='latest'
        """
        
        logger.info(f"Starting send_responses stream for session: {session_id}")
        
        try:
            async for message in ws_reader.stream(query):
                content_str = message.get("content", "{}")
                try:
                    content = json.loads(content_str)
                    text = content.get("text", "")
                except json.JSONDecodeError:
                    text = content_str
                
                logger.info(f"Sending response to WebSocket: {session_id}, text length: {len(text)}")
                
                await websocket.send_json({
                    "type": "response",
                    "text": text,
                    "message_id": message.get("id", ""),
                })
                
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected during send_responses: {session_id}")
        except Exception as e:
            logger.error(f"WebSocket send error: {e}", exc_info=True)
        finally:
            logger.info(f"send_responses ended for session: {session_id}")
    
    # Run both tasks concurrently
    receive_task = asyncio.create_task(receive_messages())
    send_task = asyncio.create_task(send_responses())
    
    try:
        await asyncio.gather(receive_task, send_task)
    except Exception:
        receive_task.cancel()
        send_task.cancel()


@router.get("/sessions/{session_id}/history")
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
