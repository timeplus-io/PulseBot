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
    user_message_preview string,-- First 200 chars
    assistant_response_preview string,
    
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
CREATE MUTABLE STREAM IF NOT EXISTS memory (
    id string,
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
    access_count int32 DEFAULT 0,
    last_accessed datetime64(3),
    expires_at datetime64(3) DEFAULT to_datetime64('2099-12-31 23:59:59', 3)
)
PRIMARY KEY (id)
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

# Materialized Views
MESSAGES_BY_SESSION_MV_DDL = """
CREATE MATERIALIZED VIEW IF NOT EXISTS messages_by_session AS
SELECT * FROM messages
ORDER BY session_id, timestamp;
"""

LLM_COST_HOURLY_MV_DDL = """
CREATE MATERIALIZED VIEW IF NOT EXISTS llm_cost_hourly AS
SELECT 
    tumble_start(timestamp, 1h) as hour,
    model,
    count() as request_count,
    sum(total_tokens) as total_tokens,
    sum(estimated_cost_usd) as total_cost_usd,
    avg(latency_ms) as avg_latency_ms
FROM llm_logs
GROUP BY hour, model;
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
        ("memory", MEMORY_STREAM_DDL),
        ("events", EVENTS_STREAM_DDL),
    ]
    
    for name, ddl in streams:
        try:
            client.execute(ddl)
            logger.info(f"Created stream: {name}")
        except Exception as e:
            logger.warning(f"Stream {name} may already exist: {e}")
    
    # Create materialized views
    views = [
        ("messages_by_session", MESSAGES_BY_SESSION_MV_DDL),
        ("llm_cost_hourly", LLM_COST_HOURLY_MV_DDL),
    ]
    
    for name, ddl in views:
        try:
            client.execute(ddl)
            logger.info(f"Created materialized view: {name}")
        except Exception as e:
            logger.warning(f"Materialized view {name} may already exist: {e}")
    
    logger.info("Timeplus streams setup complete")


async def drop_streams(client: "TimeplusClient") -> None:
    """Drop all PulseBot streams (use with caution!).
    
    Args:
        client: Timeplus client instance
    """
    logger.warning("Dropping all Timeplus streams...")
    
    # Drop views first (they depend on streams)
    views = ["messages_by_session", "llm_cost_hourly"]
    for view in views:
        try:
            client.execute(f"DROP VIEW IF EXISTS {view}")
            logger.info(f"Dropped view: {view}")
        except Exception as e:
            logger.warning(f"Could not drop view {view}: {e}")
    
    # Drop streams
    streams = ["messages", "llm_logs", "memory", "events"]
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
    required_streams = ["messages", "llm_logs", "memory", "events"]
    results = {}
    
    for stream in required_streams:
        try:
            client.query(f"SELECT 1 FROM table({stream}) LIMIT 1")
            results[stream] = True
        except Exception:
            results[stream] = False
    
    return results
