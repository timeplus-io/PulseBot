"""Tests for Timeplus stream setup DDL."""
from __future__ import annotations

from pulsebot.timeplus.setup import (
    TASKS_STREAM_DDL,
    TASK_TRIGGERS_STREAM_DDL,
)


def test_tasks_ddl_has_required_fields():
    ddl = TASKS_STREAM_DDL  # pulsebot.tasks
    for field in ("task_id", "task_name", "task_type", "prompt", "schedule",
                  "status", "created_at", "created_by"):
        assert field in ddl, f"Missing field: {field}"


def test_task_triggers_ddl_has_required_fields():
    ddl = TASK_TRIGGERS_STREAM_DDL
    for field in ("trigger_id", "task_id", "task_name", "prompt",
                  "execution_id", "triggered_at"):
        assert field in ddl, f"Missing field: {field}"


def test_create_streams_includes_new_streams(monkeypatch):
    """Verify the two new streams are set up alongside the existing ones."""
    executed = []

    class FakeClient:
        def execute(self, sql):
            executed.append(sql)

    import asyncio
    from pulsebot.timeplus.setup import create_streams
    asyncio.run(create_streams(FakeClient()))

    names = "\n".join(executed)
    assert "tasks" in names
    assert "task_triggers" in names
