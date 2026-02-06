"""Utility functions for PulseBot."""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def now_utc() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def hash_content(content: str) -> str:
    """Generate SHA256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def truncate_string(s: str, max_length: int = 200) -> str:
    """Truncate string to max length with ellipsis."""
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + "..."


def safe_json_loads(s: str, default: Any = None) -> Any:
    """Safely parse JSON string, returning default on failure."""
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return default if default is not None else {}


def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """Safely convert object to JSON string."""
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return default
