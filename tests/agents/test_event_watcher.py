"""Tests for EventWatcher."""
from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from pulsebot.agents.event_watcher import EventWatcher


def make_watcher(
    project_id="proj_test",
    event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
    context_field="payload",
    trigger_prompt="Investigate:",
    checkpoint_sn=0,
):
    project_manager = MagicMock()
    project_manager.is_project_busy.return_value = False
    project_manager.trigger_project_with_context = MagicMock()

    timeplus = MagicMock()
    config = MagicMock()
    start_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)

    with patch("pulsebot.agents.event_watcher.TimeplusClient"), \
         patch("pulsebot.agents.event_watcher.StreamReader"):
        watcher = EventWatcher(
            project_id=project_id,
            event_query=event_query,
            context_field=context_field,
            trigger_prompt=trigger_prompt,
            project_manager=project_manager,
            timeplus=timeplus,
            config=config,
            checkpoint_sn=checkpoint_sn,
            start_time=start_time,
        )
    return watcher, project_manager


def test_event_watcher_initial_query_no_checkpoint():
    watcher, _ = make_watcher(checkpoint_sn=0)
    query = watcher._build_query()
    assert "SETTINGS seek_to='2026-01-01 12:00:00'" in query
    assert "_tp_sn >" not in query


def test_event_watcher_query_with_checkpoint_and_where():
    """Query that already has WHERE: must append AND _tp_sn > N."""
    watcher, _ = make_watcher(
        event_query="SELECT payload FROM pulsebot.events WHERE severity = 'error'",
        checkpoint_sn=42,
    )
    query = watcher._build_query()
    assert "AND _tp_sn > 42" in query
    assert "seek_to='earliest'" in query


def test_event_watcher_query_with_checkpoint_no_where():
    """Query with no WHERE clause: must use WHERE _tp_sn > N (not AND)."""
    watcher, _ = make_watcher(
        event_query="SELECT payload FROM pulsebot.events",
        checkpoint_sn=42,
    )
    query = watcher._build_query()
    assert "WHERE _tp_sn > 42" in query
    assert "seek_to='earliest'" in query
    assert " AND _tp_sn" not in query


def test_event_watcher_stop_sets_running_false():
    watcher, _ = make_watcher()
    watcher._running = True
    watcher.stop()
    assert watcher._running is False


@pytest.mark.asyncio
async def test_event_watcher_triggers_when_not_busy():
    watcher, pm = make_watcher(trigger_prompt="Investigate:")
    pm.is_project_busy.return_value = False

    row = {"payload": "Connection refused", "_tp_sn": 10}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_called_once_with(
        "proj_test", "Investigate:\n\nConnection refused"
    )
    assert watcher._checkpoint_sn == 10


@pytest.mark.asyncio
async def test_event_watcher_skips_when_busy():
    watcher, pm = make_watcher()
    pm.is_project_busy.return_value = True

    row = {"payload": "some event", "_tp_sn": 5}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_not_called()
    assert watcher._checkpoint_sn == 5


@pytest.mark.asyncio
async def test_event_watcher_skips_missing_context_field():
    watcher, pm = make_watcher(context_field="payload")
    pm.is_project_busy.return_value = False

    row = {"other_field": "data", "_tp_sn": 7}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_not_called()
    assert watcher._checkpoint_sn == 7


@pytest.mark.asyncio
async def test_event_watcher_skips_empty_context_value():
    watcher, pm = make_watcher(context_field="payload")
    pm.is_project_busy.return_value = False

    row = {"payload": "", "_tp_sn": 9}
    await watcher._process_row(row)

    pm.trigger_project_with_context.assert_not_called()
    assert watcher._checkpoint_sn == 9
