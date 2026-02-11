"""Timeplus stream and schema setup for PulseBot."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


# SQL DDL for creating Timeplus streams
MESSAGES_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS messages (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    -- Routing
    source string,           -- 'telegram', 'whatsapp', 'slack', 'agent', 'skill', 'system'
    target string,           -- 'agent', 'channel:telegram', 'skill:weather', 'broadcast'
    session_id string,       -- Groups related messages
    
    -- Content
    message_type string,     -- 'user_input', 'agent_response', 'tool_call', 'tool_result', 'error'
    content string,          -- JSON payload
    
    -- Metadata
    user_id string,
    channel_metadata string, -- Channel-specific data (JSON)
    priority int8 DEFAULT 0  -- -1: low, 0: normal, 1: high, 2: urgent
) 
SETTINGS event_time_column='timestamp';
"""

LLM_LOGS_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS llm_logs (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    -- Request
    session_id string,
    model string,               -- 'claude-sonnet-4-20250514', 'gpt-4o', 'deepseek-r1'
    provider string,            -- 'anthropic', 'openai', 'openrouter'
    
    -- Tokens & Cost
    input_tokens int32,
    output_tokens int32,
    total_tokens int32,
    estimated_cost_usd float32,
    
    -- Timing
    latency_ms int32,
    time_to_first_token_ms int32 DEFAULT 0,
    
    -- Content (for debugging)
    system_prompt_hash string,  -- SHA256 of system prompt (not full content)
    system_prompt_preview string,-- First 200 chars of system prompt
    user_message_preview string,-- First 200 chars
    assistant_response_preview string,
    full_response_content string,-- Full response content for debugging
    messages_count int8,        -- Number of messages in context
    
    -- Tool Usage
    tools_called array(string),
    tool_call_count int8,
    
    -- Status
    status string,              -- 'success', 'error', 'rate_limited', 'timeout'
    error_message string DEFAULT ''
)
SETTINGS event_time_column='timestamp';
"""

MEMORY_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS memory (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),

    -- Classification
    memory_type string,         -- 'fact', 'preference', 'conversation_summary', 'skill_learned'
    category string,            -- 'user_info', 'project', 'schedule', 'general'

    -- Content
    content string,             -- The memory itself
    source_session_id string,   -- Where this memory originated

    -- Vector embedding for semantic search
    embedding array(float32),   -- 1536-dim for OpenAI, 1024 for others

    -- Lifecycle
    importance float32,         -- 0.0 to 1.0, affects retrieval priority
    is_deleted bool DEFAULT false  -- Soft delete flag (append-only stream)
)
SETTINGS event_time_column='timestamp';
"""

TOOL_LOGS_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS tool_logs (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),

    -- Context
    session_id string,
    llm_request_id string,      -- Links to the LLM call that triggered this

    -- Tool Info
    tool_name string,
    skill_name string,
    arguments string,           -- JSON of tool arguments

    -- Result
    status string,              -- 'started', 'success', 'error'
    result_preview string,      -- First 500 chars of result
    error_message string DEFAULT '',

    -- Timing
    duration_ms int32 DEFAULT 0
)
SETTINGS event_time_column='timestamp';
"""

EVENTS_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS events (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    event_type string,          -- 'heartbeat', 'channel_connected', 'skill_loaded', 'error', 'alert'
    source string,
    severity string,            -- 'debug', 'info', 'warning', 'error', 'critical'
    
    payload string,             -- JSON event data
    
    -- For filtering
    tags array(string)
)
SETTINGS event_time_column='timestamp';
"""

async def create_streams(client: "TimeplusClient") -> None:
    """Create all required Timeplus streams.
    
    Args:
        client: Timeplus client instance
    """
    logger.info("Creating Timeplus streams...")
    
    # Create streams
    streams = [
        ("messages", MESSAGES_STREAM_DDL),
        ("llm_logs", LLM_LOGS_STREAM_DDL),
        ("tool_logs", TOOL_LOGS_STREAM_DDL),
        ("memory", MEMORY_STREAM_DDL),
        ("events", EVENTS_STREAM_DDL),
    ]
    
    for name, ddl in streams:
        try:
            client.execute(ddl)
            logger.info(f"Created stream: {name}")
        except Exception as e:
            logger.warning(f"Stream {name} may already exist: {e}")

    logger.info("Timeplus streams setup complete")


async def drop_streams(client: "TimeplusClient") -> None:
    """Drop all PulseBot streams (use with caution!).

    Args:
        client: Timeplus client instance
    """
    logger.warning("Dropping all Timeplus streams...")

    # Drop streams
    streams = ["messages", "llm_logs", "tool_logs", "memory", "events"]
    for stream in streams:
        try:
            client.execute(f"DROP STREAM IF EXISTS {stream}")
            logger.info(f"Dropped stream: {stream}")
        except Exception as e:
            logger.warning(f"Could not drop stream {stream}: {e}")
    
    logger.info("All streams dropped")


def verify_streams(client: "TimeplusClient") -> dict[str, bool]:
    """Verify that all required streams exist.
    
    Args:
        client: Timeplus client instance
        
    Returns:
        Dictionary mapping stream names to existence status
    """
    required_streams = ["messages", "llm_logs", "tool_logs", "memory", "events"]
    results = {}
    
    for stream in required_streams:
        try:
            client.query(f"SELECT 1 FROM table({stream}) LIMIT 1")
            results[stream] = True
        except Exception:
            results[stream] = False
    
    return results
