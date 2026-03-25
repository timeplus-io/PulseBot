# Multi-Agent Support (Phases 1 & 2) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add kanban-stream-based multi-agent coordination to PulseBot, allowing the main agent to spawn a Manager Agent and worker sub-agents that collaborate through a dedicated `kanban` Timeplus stream.

**Architecture:** A new `pulsebot/agents/` module provides `SubAgent`, `ManagerAgent`, and `ProjectManager` classes. The main `Agent` class is **not modified**. All inter-agent communication flows through the `pulsebot.kanban` stream. A new `project_manager` built-in skill exposes `create_project`, `list_projects`, `cancel_project`, and `get_project_status` tools to the main agent.

**Tech Stack:** Python asyncio (tasks for sub-agents), Timeplus streams (kanban, kanban_projects, kanban_agents), existing `StreamReader`/`StreamWriter`, `LLMProvider`, `ToolExecutor`, `SkillLoader`.

---

## Scope

- **In scope**: Phases 1 & 2 from the design doc — streams, models, SubAgent, ManagerAgent, ProjectManager, project_manager skill, factory wiring, unit tests.
- **Out of scope**: REST API endpoints (Phase 3), WebSocket extensions (Phase 3), load testing (Phase 4).

## Key Conventions

- **Agent ID derivation**: `name.lower().replace(" ", "_")` prefixed with `agent_` → `"Analyst"` → `"agent_analyst"`. Caller is responsible for unique names within a project. Manager is always `f"manager_{project_id}"`.
- **agent.py**: UNCHANGED — the main agent never touches the kanban stream.
- **Sub-agent LLM loop**: Standalone `_reason()` method in `SubAgent` — not extracted from `Agent`. Mirrors the core logic without broadcasting or memory.
- **Skill resolution**: If `spec.skills is None` → inherit all from parent loader. If explicit list → create fresh `SkillLoader` with only those skills.
- **Hook inheritance**: Sub-agents reuse the same `ToolExecutor` instance as the main agent (passed by `ProjectManager`). Hook chain is inherited automatically.

---

## Task 1: Stream DDL + MultiAgentConfig

**Files:**
- Modify: `pulsebot/timeplus/setup.py`
- Modify: `pulsebot/config.py`
- Test: `tests/test_multi_agent_setup.py`

### Step 1: Write the failing test

```python
# tests/test_multi_agent_setup.py
"""Tests for multi-agent stream DDL and config."""

import pytest
from pulsebot.config import Config, MultiAgentConfig
from pulsebot.timeplus.setup import (
    KANBAN_STREAM_DDL,
    KANBAN_PROJECTS_STREAM_DDL,
    KANBAN_AGENTS_STREAM_DDL,
)


def test_kanban_ddl_has_required_fields():
    assert "msg_id" in KANBAN_STREAM_DDL
    assert "project_id" in KANBAN_STREAM_DDL
    assert "sender_id" in KANBAN_STREAM_DDL
    assert "target_id" in KANBAN_STREAM_DDL
    assert "msg_type" in KANBAN_STREAM_DDL
    assert "content" in KANBAN_STREAM_DDL


def test_kanban_projects_ddl_has_required_fields():
    assert "project_id" in KANBAN_PROJECTS_STREAM_DDL
    assert "status" in KANBAN_PROJECTS_STREAM_DDL
    assert "session_id" in KANBAN_PROJECTS_STREAM_DDL
    assert "agent_ids" in KANBAN_PROJECTS_STREAM_DDL


def test_kanban_agents_ddl_has_required_fields():
    assert "agent_id" in KANBAN_AGENTS_STREAM_DDL
    assert "project_id" in KANBAN_AGENTS_STREAM_DDL
    assert "role" in KANBAN_AGENTS_STREAM_DDL
    assert "checkpoint_sn" in KANBAN_AGENTS_STREAM_DDL
    assert "skills" in KANBAN_AGENTS_STREAM_DDL


def test_multi_agent_config_defaults():
    cfg = MultiAgentConfig()
    assert cfg.enabled is True
    assert cfg.max_agents_per_project == 10
    assert cfg.max_concurrent_projects == 5
    assert cfg.default_agent_timeout == 300
    assert cfg.project_timeout == 1800
    assert cfg.checkpoint_interval == 1


def test_config_includes_multi_agent():
    cfg = Config()
    assert hasattr(cfg, "multi_agent")
    assert isinstance(cfg.multi_agent, MultiAgentConfig)
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_multi_agent_setup.py -v
```

Expected: `ImportError: cannot import name 'KANBAN_STREAM_DDL'`

### Step 3: Add stream DDLs to setup.py

Add to `pulsebot/timeplus/setup.py` (after existing DDL constants):

```python
KANBAN_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS pulsebot.kanban (
    msg_id        string DEFAULT uuid(),
    timestamp     datetime64(3) DEFAULT now64(3),
    project_id    string,
    sender_id     string,
    target_id     string,
    msg_type      string,
    content       string,
    priority      int8 DEFAULT 0,
    metadata      string DEFAULT '{}'
)
SETTINGS event_time_column='timestamp';
"""

KANBAN_PROJECTS_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS pulsebot.kanban_projects (
    project_id      string DEFAULT uuid(),
    timestamp       datetime64(3) DEFAULT now64(3),
    name            string,
    description     string,
    status          string,
    created_by      string,
    session_id      string,
    agent_ids       array(string),
    config_overrides string DEFAULT '{}'
)
SETTINGS event_time_column='timestamp';
"""

KANBAN_AGENTS_STREAM_DDL = """
CREATE STREAM IF NOT EXISTS pulsebot.kanban_agents (
    agent_id        string,
    timestamp       datetime64(3) DEFAULT now64(3),
    project_id      string,
    name            string,
    role            string,
    task_description string,
    target_agents   array(string),
    status          string,
    config          string DEFAULT '{}',
    skills          array(string),
    skill_overrides string DEFAULT '{}',
    checkpoint_sn   uint64 DEFAULT 0,
    metadata        string DEFAULT '{}'
)
SETTINGS event_time_column='timestamp';
"""
```

### Step 4: Add MultiAgentConfig to config.py

Add to `pulsebot/config.py` (before the `Config` class):

```python
class MultiAgentConfig(BaseModel):
    """Multi-agent coordination configuration."""
    enabled: bool = True
    max_agents_per_project: int = 10
    max_concurrent_projects: int = 5
    default_agent_timeout: int = 300
    project_timeout: int = 1800
    checkpoint_interval: int = 1
```

Add to the `Config` class:
```python
multi_agent: MultiAgentConfig = Field(default_factory=MultiAgentConfig)
```

### Step 5: Run tests to verify they pass

```bash
pytest tests/test_multi_agent_setup.py -v
```

Expected: All 5 tests PASS.

### Step 6: Commit

```bash
git add pulsebot/timeplus/setup.py pulsebot/config.py tests/test_multi_agent_setup.py
git commit -m "feat: add kanban stream DDL and MultiAgentConfig"
```

---

## Task 2: SubAgentSpec and ProjectState Models

**Files:**
- Create: `pulsebot/agents/__init__.py`
- Create: `pulsebot/agents/models.py`
- Test: `tests/test_multi_agent_models.py`

### Step 1: Write the failing test

```python
# tests/test_multi_agent_models.py
"""Tests for multi-agent data models."""

import pytest
from pulsebot.agents.models import SubAgentSpec, ProjectState


def test_subagentspec_default_agent_id_derived_from_name():
    spec = SubAgentSpec(
        name="SQL Analyst",
        task_description="Analyze data",
        project_id="proj_001",
        target_agents=[],
    )
    assert spec.agent_id == "agent_sql_analyst"


def test_subagentspec_explicit_agent_id_overrides_derivation():
    spec = SubAgentSpec(
        name="Analyst",
        agent_id="my_custom_id",
        task_description="Analyze data",
        project_id="proj_001",
        target_agents=[],
    )
    assert spec.agent_id == "my_custom_id"


def test_subagentspec_defaults():
    spec = SubAgentSpec(
        name="Researcher",
        task_description="Research things",
        project_id="proj_001",
        target_agents=["agent_analyst"],
    )
    assert spec.role == "worker"
    assert spec.model is None
    assert spec.provider is None
    assert spec.temperature is None
    assert spec.max_iterations == 5
    assert spec.enable_memory is False
    assert spec.skills is None
    assert spec.skill_overrides is None
    assert spec.timeout_seconds == 300
    assert spec.checkpoint_sn == 0


def test_subagentspec_with_skill_overrides():
    spec = SubAgentSpec(
        name="Shell Worker",
        task_description="Run commands",
        project_id="proj_001",
        target_agents=[],
        skills=["shell"],
        skill_overrides={"shell": {"allowed_commands": ["grep"]}},
    )
    assert spec.skills == ["shell"]
    assert spec.skill_overrides["shell"]["allowed_commands"] == ["grep"]


def test_projectstate_fields():
    state = ProjectState(
        project_id="proj_abc",
        name="Test Project",
        description="A test",
        session_id="sess_123",
        agent_ids=["agent_a", "agent_b"],
    )
    assert state.status == "active"
    assert state.project_id == "proj_abc"
    assert "agent_a" in state.agent_ids
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_multi_agent_models.py -v
```

Expected: `ModuleNotFoundError: No module named 'pulsebot.agents'`

### Step 3: Create the agents package

```python
# pulsebot/agents/__init__.py
"""Multi-agent coordination module for PulseBot."""

from pulsebot.agents.models import ProjectState, SubAgentSpec

__all__ = ["SubAgentSpec", "ProjectState"]
```

```python
# pulsebot/agents/models.py
"""Data models for the multi-agent system."""

from __future__ import annotations

from dataclasses import dataclass, field


def _derive_agent_id(name: str) -> str:
    """Derive a stable agent ID from a human-readable name.

    'SQL Analyst' → 'agent_sql_analyst'
    'Report Writer' → 'agent_report_writer'
    """
    slug = name.lower().replace(" ", "_").replace("-", "_")
    return f"agent_{slug}"


@dataclass
class SubAgentSpec:
    """Specification for creating a sub-agent."""

    # Identity
    name: str
    task_description: str
    project_id: str
    target_agents: list[str]

    # Auto-derived from name if not provided
    agent_id: str = ""
    role: str = "worker"  # "manager" or "worker"

    # LLM overrides (None = inherit from main agent config)
    model: str | None = None
    provider: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    max_iterations: int = 5
    enable_memory: bool = False

    # Skill configuration (None = inherit all from main agent)
    skills: list[str] | None = None
    skill_overrides: dict | None = None

    # Execution
    timeout_seconds: int = 300
    checkpoint_sn: int = 0

    def __post_init__(self) -> None:
        if not self.agent_id:
            self.agent_id = _derive_agent_id(self.name)


@dataclass
class ProjectState:
    """Runtime state of a multi-agent project."""

    project_id: str
    name: str
    description: str
    session_id: str
    agent_ids: list[str]
    status: str = "active"  # 'active', 'completed', 'failed', 'cancelled'
    config_overrides: dict = field(default_factory=dict)
```

### Step 4: Run tests to verify they pass

```bash
pytest tests/test_multi_agent_models.py -v
```

Expected: All 5 tests PASS.

### Step 5: Commit

```bash
git add pulsebot/agents/__init__.py pulsebot/agents/models.py tests/test_multi_agent_models.py
git commit -m "feat: add SubAgentSpec and ProjectState models"
```

---

## Task 3: SkillLoader Extensions

The design doc's `_resolve_skills()` needs two operations on `SkillLoader`:
1. Get all currently loaded skills (for inherit-all case).
2. Create a scoped loader with only named skills (for explicit-list case).

**Files:**
- Modify: `pulsebot/skills/loader.py`
- Test: `tests/test_skill_loader_extensions.py`

### Step 1: Write the failing test

```python
# tests/test_skill_loader_extensions.py
"""Tests for SkillLoader extensions needed by multi-agent system."""

import pytest
from pulsebot.skills.loader import SkillLoader
from pulsebot.skills.builtin.file_ops import FileOpsSkill
from pulsebot.skills.builtin.shell import ShellSkill


@pytest.fixture
def loader_with_two_skills():
    loader = SkillLoader()
    loader.load_builtin("file_ops")
    loader.load_builtin("shell")
    return loader


def test_get_loaded_skills_returns_all_skills(loader_with_two_skills):
    skills = loader_with_two_skills.get_loaded_skills()
    names = {s.name for s in skills}
    assert "file_ops" in names
    assert "shell" in names


def test_get_loaded_skills_empty_loader():
    loader = SkillLoader()
    assert loader.get_loaded_skills() == []


def test_create_subset_returns_only_named_skills(loader_with_two_skills):
    subset = loader_with_two_skills.create_subset(["file_ops"])
    skills = subset.get_loaded_skills()
    names = {s.name for s in skills}
    assert names == {"file_ops"}


def test_create_subset_excludes_unknown_names(loader_with_two_skills):
    # Unknown names are silently skipped (not loaded in parent either)
    subset = loader_with_two_skills.create_subset(["file_ops", "nonexistent"])
    skills = subset.get_loaded_skills()
    names = {s.name for s in skills}
    assert names == {"file_ops"}


def test_create_subset_preserves_tool_routing(loader_with_two_skills):
    subset = loader_with_two_skills.create_subset(["shell"])
    # Shell tools should be routable
    skill = subset.get_skill_for_tool("run_command")
    assert skill is not None
    assert skill.name == "shell"


def test_create_subset_empty_list(loader_with_two_skills):
    subset = loader_with_two_skills.create_subset([])
    assert subset.get_loaded_skills() == []
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_skill_loader_extensions.py -v
```

Expected: `AttributeError: 'SkillLoader' object has no attribute 'get_loaded_skills'`

### Step 3: Add methods to SkillLoader

Add to `pulsebot/skills/loader.py` after `get_tool_definitions()`:

```python
def get_loaded_skills(self) -> list[BaseSkill]:
    """Return all currently loaded skill instances.

    Returns:
        List of loaded BaseSkill instances.
    """
    return list(self._skills.values())

def create_subset(self, names: list[str]) -> "SkillLoader":
    """Create a new SkillLoader containing only the named skills.

    Skills not present in this loader are silently skipped.
    Useful for sub-agent skill isolation.

    Args:
        names: Skill names to include.

    Returns:
        New SkillLoader with only the named skills.
    """
    subset = SkillLoader()
    for name in names:
        skill = self._skills.get(name)
        if skill is None:
            logger.warning(f"Skill '{name}' not found in loader, skipping")
            continue
        subset._skills[name] = skill
        for tool in skill.get_tools():
            subset._tool_to_skill[tool.name] = name
    return subset
```

### Step 4: Run tests to verify they pass

```bash
pytest tests/test_skill_loader_extensions.py -v
```

Expected: All 6 tests PASS.

### Step 5: Run full suite to check no regressions

```bash
pytest -x -q
```

Expected: All existing tests still pass.

### Step 6: Commit

```bash
git add pulsebot/skills/loader.py tests/test_skill_loader_extensions.py
git commit -m "feat: add get_loaded_skills() and create_subset() to SkillLoader"
```

---

## Task 4: SubAgent

**Files:**
- Create: `pulsebot/agents/sub_agent.py`
- Test: `tests/test_sub_agent.py`

### Step 1: Write the failing test

```python
# tests/test_sub_agent.py
"""Tests for SubAgent class."""

from __future__ import annotations

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pulsebot.agents.models import SubAgentSpec
from pulsebot.agents.sub_agent import SubAgent
from pulsebot.providers.base import LLMResponse, Usage


@pytest.fixture
def spec():
    return SubAgentSpec(
        name="Analyst",
        task_description="Analyze things",
        project_id="proj_001",
        target_agents=[],
    )


@pytest.fixture
def mock_timeplus():
    client = MagicMock()
    client.query = MagicMock(return_value=[])
    return client


@pytest.fixture
def mock_llm():
    provider = MagicMock()
    provider.provider_name = "test"
    provider.model = "test-model"
    provider.get_tool_definitions = MagicMock(return_value=[])
    provider.chat = AsyncMock(return_value=LLMResponse(
        content="Analysis complete.",
        tool_calls=None,
        usage=Usage(input_tokens=10, output_tokens=5),
    ))
    return provider


@pytest.fixture
def mock_skill_loader():
    loader = MagicMock()
    loader.get_loaded_skills = MagicMock(return_value=[])
    loader.create_subset = MagicMock(return_value=MagicMock(
        get_tools=MagicMock(return_value=[]),
        get_loaded_skills=MagicMock(return_value=[]),
    ))
    loader.get_tools = MagicMock(return_value=[])
    return loader


@pytest.fixture
def mock_executor():
    executor = MagicMock()
    executor.execute = AsyncMock(return_value={"success": True, "output": "done", "error": ""})
    return executor


@pytest.fixture
def mock_config():
    config = MagicMock()
    config.agent.model = "claude-sonnet-4-20250514"
    config.agent.provider = "anthropic"
    config.agent.temperature = 0.7
    config.agent.max_tokens = 4096
    return config


def make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"):
        return SubAgent(
            spec=spec,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )


def test_sub_agent_agent_id_from_spec(spec, mock_timeplus, mock_llm,
                                       mock_skill_loader, mock_executor, mock_config):
    agent = make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader,
                       mock_executor, mock_config)
    assert agent.agent_id == "agent_analyst"
    assert agent.project_id == "proj_001"


def test_sub_agent_inherits_all_skills_when_spec_skills_is_none(
        spec, mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    """When spec.skills is None, SubAgent uses the full parent skill_loader."""
    agent = make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader,
                       mock_executor, mock_config)
    # create_subset should NOT have been called (inherited all)
    mock_skill_loader.create_subset.assert_not_called()


def test_sub_agent_creates_subset_when_skills_specified(
        mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    spec = SubAgentSpec(
        name="Shell Worker",
        task_description="Run commands",
        project_id="proj_001",
        target_agents=[],
        skills=["shell"],
    )
    agent = make_agent(spec, mock_timeplus, mock_llm, mock_skill_loader,
                       mock_executor, mock_config)
    mock_skill_loader.create_subset.assert_called_once_with(["shell"])


@pytest.mark.asyncio
async def test_process_task_calls_llm_and_writes_to_kanban(
        spec, mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter") as MockWriter:
        mock_writer_instance = AsyncMock()
        mock_writer_instance.write = AsyncMock()
        MockWriter.return_value = mock_writer_instance

        agent = SubAgent(
            spec=spec,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )
        # Manually set kanban_writer to the mock
        agent.kanban_writer = mock_writer_instance
        agent.agents_writer = mock_writer_instance

        message = {
            "msg_id": "msg_001",
            "project_id": "proj_001",
            "sender_id": "manager_proj_001",
            "target_id": "agent_analyst",
            "msg_type": "task",
            "content": "Analyze the data",
            "_tp_sn": 42,
        }

        await agent._process_task(message)

        # LLM should have been called
        mock_llm.chat.assert_called_once()

        # Result should have been written to kanban
        mock_writer_instance.write.assert_called()
        write_call = mock_writer_instance.write.call_args[0][0]
        assert write_call["msg_type"] == "result"
        assert write_call["sender_id"] == "agent_analyst"
        assert write_call["content"] == "Analysis complete."


@pytest.mark.asyncio
async def test_process_task_routes_to_target_agents(
        mock_timeplus, mock_llm, mock_skill_loader, mock_executor, mock_config):
    spec = SubAgentSpec(
        name="Researcher",
        task_description="Research",
        project_id="proj_001",
        target_agents=["agent_analyst"],
    )
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter") as MockWriter:
        mock_writer_instance = AsyncMock()
        MockWriter.return_value = mock_writer_instance

        agent = SubAgent(
            spec=spec,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )
        agent.kanban_writer = mock_writer_instance
        agent.agents_writer = mock_writer_instance

        message = {
            "msg_id": "msg_001",
            "project_id": "proj_001",
            "sender_id": "manager_proj_001",
            "target_id": "agent_researcher",
            "msg_type": "task",
            "content": "Research AI",
            "_tp_sn": 1,
        }
        await agent._process_task(message)

        write_call = mock_writer_instance.write.call_args_list[0][0][0]
        assert write_call["target_id"] == "agent_analyst"
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_sub_agent.py -v
```

Expected: `ModuleNotFoundError: No module named 'pulsebot.agents.sub_agent'`

### Step 3: Implement SubAgent

```python
# pulsebot/agents/sub_agent.py
"""SubAgent: a worker agent that reads from kanban and writes results back."""

from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from pulsebot.timeplus.streams import StreamReader, StreamWriter
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.agents.models import SubAgentSpec
    from pulsebot.config import Config
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class SubAgent:
    """
    A sub-agent that participates in a multi-agent project.

    Reads task messages from the kanban stream, processes them through
    an LLM + tool loop, and writes results back to kanban.
    """

    def __init__(
        self,
        spec: "SubAgentSpec",
        timeplus: "TimeplusClient",
        llm_provider: "LLMProvider",
        skill_loader: "SkillLoader",
        executor: "ToolExecutor",
        config: "Config",
    ) -> None:
        from pulsebot.timeplus.client import TimeplusClient

        self.spec = spec
        self.agent_id = spec.agent_id
        self.project_id = spec.project_id

        # Resolve LLM provider (override model/provider if specified)
        self.llm = self._resolve_provider(spec, llm_provider, config)

        # Resolve skill set for this sub-agent
        self._skill_loader = self._resolve_skills(spec, skill_loader)
        self.executor = executor

        # Use a dedicated batch client for writes to avoid conflicts with
        # the streaming query connection.
        batch_client = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )

        self.kanban_reader = StreamReader(timeplus, "kanban")
        self.kanban_writer = StreamWriter(batch_client, "kanban")
        self.agents_writer = StreamWriter(batch_client, "kanban_agents")

        self._checkpoint_sn: int = spec.checkpoint_sn
        self._running = False
        self._batch_client = batch_client

    def _resolve_provider(
        self,
        spec: "SubAgentSpec",
        default_provider: "LLMProvider",
        config: "Config",
    ) -> "LLMProvider":
        """Use spec overrides if set; otherwise inherit the main provider."""
        if spec.model is None and spec.provider is None:
            return default_provider
        # Re-create provider with overrides applied
        from pulsebot.factory import create_provider
        import copy
        overridden = copy.deepcopy(config)
        if spec.provider:
            overridden.agent.provider = spec.provider
        if spec.model:
            overridden.agent.model = spec.model
        if spec.temperature is not None:
            overridden.agent.temperature = spec.temperature
        if spec.max_tokens is not None:
            overridden.agent.max_tokens = spec.max_tokens
        return create_provider(overridden)

    def _resolve_skills(
        self,
        spec: "SubAgentSpec",
        skill_loader: "SkillLoader",
    ) -> "SkillLoader":
        """Return the appropriate SkillLoader for this sub-agent.

        - spec.skills is None  → inherit all skills from parent loader
        - spec.skills is a list → create subset with only those skills
        """
        if spec.skills is None:
            return skill_loader
        return skill_loader.create_subset(spec.skills)

    def _get_manager_id(self) -> str:
        return f"manager_{self.project_id}"

    def _build_system_prompt(self) -> str:
        tools = self._skill_loader.get_tools()
        tools_text = ""
        if tools:
            tools_text = "\n\nAvailable tools:\n" + "\n".join(
                f"- {t.name}: {t.description}" for t in tools
            )
        return self.spec.task_description + tools_text

    async def run(self) -> None:
        """Main event loop — pull tasks from kanban, process, push results."""
        self._running = True

        sn_filter = (
            f"AND _tp_sn > {self._checkpoint_sn}"
            if self._checkpoint_sn > 0
            else ""
        )
        query = f"""
        SELECT *, _tp_sn FROM pulsebot.kanban
        WHERE target_id = '{self.agent_id}'
        AND project_id = '{self.project_id}'
        AND msg_type IN ('task', 'control')
        {sn_filter}
        SETTINGS seek_to='latest'
        """

        logger.info(f"SubAgent {self.agent_id} starting kanban loop")

        async for message in self.kanban_reader.stream(query):
            if not self._running:
                break

            msg_type = message.get("msg_type", "")
            try:
                if msg_type == "control":
                    await self._handle_control(message)
                elif msg_type == "task":
                    await self._process_task(message)
            except Exception as e:
                logger.error(
                    f"SubAgent {self.agent_id} error processing message: {e}",
                    exc_info=True,
                )
                await self._write_error(message, str(e))

            self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
            await self._persist_checkpoint()

    async def _handle_control(self, message: dict[str, Any]) -> None:
        """Handle control messages (cancel, pause, resume)."""
        command = message.get("content", "").strip().lower()
        if command == "cancel":
            logger.info(f"SubAgent {self.agent_id} received cancel")
            self._running = False
        else:
            logger.warning(f"SubAgent {self.agent_id} unknown control: {command!r}")

    async def _process_task(self, message: dict[str, Any]) -> None:
        """Process a task message: run LLM loop, write result to kanban."""
        content = message.get("content", "")
        system_prompt = self._build_system_prompt()

        result_text = await self._reason(system_prompt, content)

        targets = self.spec.target_agents or [self._get_manager_id()]
        for target in targets:
            await self.kanban_writer.write({
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": target,
                "msg_type": "result",
                "content": result_text,
                "metadata": json.dumps({
                    "source_msg_id": message.get("msg_id", ""),
                }),
            })

    async def _reason(self, system_prompt: str, user_content: str) -> str:
        """Run the LLM + tool loop for a single task.

        Returns the final text response.
        """
        raw_tools = self._skill_loader.get_tools()
        tools = self.llm.get_tool_definitions(raw_tools) if raw_tools else None

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": user_content}
        ]

        for _ in range(self.spec.max_iterations):
            response = await self.llm.chat(
                messages=messages,
                system=system_prompt,
                tools=tools,
            )

            if response.tool_calls:
                # Add assistant turn with tool calls
                tool_call_dicts = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    for tc in response.tool_calls
                ]
                messages.append({
                    "role": "assistant",
                    "content": response.content or "",
                    "tool_calls": tool_call_dicts,
                })

                # Execute tools and add results
                for tc in response.tool_calls:
                    result = await self.executor.execute(
                        tool_name=tc.name,
                        arguments=tc.arguments,
                        session_id=f"{self.project_id}:{self.agent_id}",
                    )
                    result_str = (
                        str(result.get("output", ""))
                        if result.get("success")
                        else f"Error: {result.get('error', '')}"
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result_str,
                    })
            else:
                return response.content or ""

        # Max iterations reached — return last content
        return response.content or ""  # type: ignore[possibly-undefined]

    async def _write_error(self, source_message: dict, error: str) -> None:
        """Write an error message to kanban targeting the manager."""
        await self.kanban_writer.write({
            "project_id": self.project_id,
            "sender_id": self.agent_id,
            "target_id": self._get_manager_id(),
            "msg_type": "error",
            "content": error,
            "metadata": json.dumps({
                "source_msg_id": source_message.get("msg_id", ""),
            }),
        })

    async def _load_checkpoint(self) -> int:
        """Load last checkpoint from kanban_agents stream."""
        rows = self._batch_client.query(f"""
            SELECT checkpoint_sn FROM table(pulsebot.kanban_agents)
            WHERE agent_id = '{self.agent_id}'
            AND project_id = '{self.project_id}'
            ORDER BY timestamp DESC LIMIT 1
        """)
        return rows[0]["checkpoint_sn"] if rows else 0

    async def _persist_checkpoint(self) -> None:
        """Write current checkpoint to agent metadata stream."""
        await self.agents_writer.write({
            "agent_id": self.agent_id,
            "project_id": self.project_id,
            "name": self.spec.name,
            "role": self.spec.role,
            "task_description": self.spec.task_description,
            "target_agents": self.spec.target_agents,
            "status": "running",
            "skills": self.spec.skills or [],
            "skill_overrides": json.dumps(self.spec.skill_overrides or {}),
            "config": json.dumps({
                "model": self.spec.model,
                "provider": self.spec.provider,
                "temperature": self.spec.temperature,
                "max_tokens": self.spec.max_tokens,
                "max_iterations": self.spec.max_iterations,
                "enable_memory": self.spec.enable_memory,
            }),
            "checkpoint_sn": self._checkpoint_sn,
        })

    async def stop(self) -> None:
        """Stop this sub-agent and persist final checkpoint."""
        self._running = False
        await self._persist_checkpoint()
```

### Step 4: Run tests to verify they pass

```bash
pytest tests/test_sub_agent.py -v
```

Expected: All tests PASS.

### Step 5: Run full suite

```bash
pytest -x -q
```

### Step 6: Commit

```bash
git add pulsebot/agents/sub_agent.py tests/test_sub_agent.py
git commit -m "feat: implement SubAgent with kanban read/LLM loop/write"
```

---

## Task 5: ManagerAgent

**Files:**
- Create: `pulsebot/agents/manager_agent.py`
- Test: `tests/test_manager_agent.py`

### Step 1: Write the failing test

```python
# tests/test_manager_agent.py
"""Tests for ManagerAgent class."""

from __future__ import annotations

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pulsebot.agents.models import SubAgentSpec
from pulsebot.providers.base import LLMResponse, Usage


@pytest.fixture
def manager_spec():
    return SubAgentSpec(
        name="Manager",
        agent_id="manager_proj_001",
        role="manager",
        task_description="Coordinate the project",
        project_id="proj_001",
        target_agents=[],
    )


@pytest.fixture
def worker_specs():
    return [
        SubAgentSpec(
            name="Analyst",
            task_description="Analyze",
            project_id="proj_001",
            target_agents=[],
        )
    ]


@pytest.fixture
def mock_timeplus():
    client = MagicMock()
    client.host = "localhost"
    client.port = 8463
    client.username = "default"
    client.password = ""
    client.query = MagicMock(return_value=[])
    return client


@pytest.fixture
def mock_config():
    cfg = MagicMock()
    cfg.agent.model = "claude-sonnet-4-20250514"
    cfg.agent.provider = "anthropic"
    cfg.agent.temperature = 0.7
    cfg.agent.max_tokens = 4096
    return cfg


def make_manager(manager_spec, worker_specs, mock_timeplus, mock_config, session_id="sess_001"):
    mock_llm = MagicMock()
    mock_llm.provider_name = "test"
    mock_llm.model = "test"
    mock_llm.get_tool_definitions = MagicMock(return_value=[])
    mock_skill_loader = MagicMock()
    mock_skill_loader.get_loaded_skills = MagicMock(return_value=[])
    mock_skill_loader.create_subset = MagicMock(return_value=MagicMock(
        get_tools=MagicMock(return_value=[]),
        get_loaded_skills=MagicMock(return_value=[]),
    ))
    mock_skill_loader.get_tools = MagicMock(return_value=[])
    mock_executor = MagicMock()

    from pulsebot.agents.manager_agent import ManagerAgent
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter"):
        return ManagerAgent(
            spec=manager_spec,
            worker_specs=worker_specs,
            session_id=session_id,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )


def test_manager_agent_has_messages_writer(manager_spec, worker_specs,
                                            mock_timeplus, mock_config):
    manager = make_manager(manager_spec, worker_specs, mock_timeplus, mock_config)
    assert hasattr(manager, "messages_writer")
    assert hasattr(manager, "session_id")
    assert manager.session_id == "sess_001"


@pytest.mark.asyncio
async def test_deliver_result_writes_to_messages_stream(
        manager_spec, worker_specs, mock_timeplus, mock_config):
    from pulsebot.agents.manager_agent import ManagerAgent
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter") as MockWriter:
        mock_writer = AsyncMock()
        MockWriter.return_value = mock_writer

        mock_llm = MagicMock()
        mock_llm.get_tool_definitions = MagicMock(return_value=[])
        mock_skill_loader = MagicMock()
        mock_skill_loader.get_loaded_skills = MagicMock(return_value=[])
        mock_skill_loader.get_tools = MagicMock(return_value=[])
        mock_executor = MagicMock()

        manager = ManagerAgent(
            spec=manager_spec,
            worker_specs=worker_specs,
            session_id="sess_001",
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
            config=mock_config,
        )
        manager.messages_writer = mock_writer

        result_message = {
            "msg_id": "msg_final",
            "content": "## Final Report\n\nSummary here.",
            "sender_id": "agent_analyst",
        }
        await manager._deliver_result(result_message)

        mock_writer.write.assert_called_once()
        write_args = mock_writer.write.call_args[0][0]
        assert write_args["session_id"] == "sess_001"
        assert write_args["target"] == "user"
        assert "Final Report" in write_args["content"]
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_manager_agent.py -v
```

Expected: `ModuleNotFoundError: No module named 'pulsebot.agents.manager_agent'`

### Step 3: Implement ManagerAgent

```python
# pulsebot/agents/manager_agent.py
"""ManagerAgent: coordinates a project and bridges kanban ↔ messages."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pulsebot.agents.sub_agent import SubAgent
from pulsebot.timeplus.streams import StreamWriter
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.agents.models import SubAgentSpec
    from pulsebot.config import Config
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class ManagerAgent(SubAgent):
    """
    A special sub-agent that coordinates a project.

    Responsibilities:
    1. Dispatch initial task messages to worker agents via kanban.
    2. Listen on kanban for results/errors from workers.
    3. Write the final result to pulsebot.messages for the main agent.
    4. Cancel all workers and mark project complete/failed.
    """

    def __init__(
        self,
        spec: "SubAgentSpec",
        worker_specs: list["SubAgentSpec"],
        session_id: str,
        timeplus: "TimeplusClient",
        llm_provider: "LLMProvider",
        skill_loader: "SkillLoader",
        executor: "ToolExecutor",
        config: "Config",
        initial_messages: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(spec, timeplus, llm_provider, skill_loader, executor, config)
        self.worker_specs = worker_specs
        self.session_id = session_id
        self.initial_messages = initial_messages or []

        # Extra writer for the messages stream
        self.messages_writer = StreamWriter(self._batch_client, "messages")
        self.projects_writer = StreamWriter(self._batch_client, "kanban_projects")

    async def run(self) -> None:
        """Manager event loop: dispatch tasks, collect results, deliver output."""
        self._running = True

        # Write initial task messages to kanban
        await self._dispatch_initial_tasks()

        query = f"""
        SELECT *, _tp_sn FROM pulsebot.kanban
        WHERE target_id = '{self.agent_id}'
        AND project_id = '{self.project_id}'
        AND msg_type IN ('result', 'error', 'status')
        SETTINGS seek_to='latest'
        """

        logger.info(f"ManagerAgent {self.agent_id} listening for results")

        async for message in self.kanban_reader.stream(query):
            if not self._running:
                break

            msg_type = message.get("msg_type", "")

            if msg_type == "result":
                await self._deliver_result(message)
                await self._complete_project()
                break
            elif msg_type == "error":
                await self._handle_worker_error(message)
                break
            elif msg_type == "status":
                await self._forward_status(message)

            self._checkpoint_sn = message.get("_tp_sn", self._checkpoint_sn)
            await self._persist_checkpoint()

    async def _dispatch_initial_tasks(self) -> None:
        """Write the initial task messages to the kanban stream."""
        for msg in self.initial_messages:
            target = msg.get("target", "")
            content = msg.get("content", "")
            if not target:
                logger.warning("Initial message missing 'target' field, skipping")
                continue
            await self.kanban_writer.write({
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": target,
                "msg_type": "task",
                "content": content,
            })
            logger.info(f"Dispatched task to {target}")

    async def _deliver_result(self, message: dict[str, Any]) -> None:
        """Write the final result to pulsebot.messages for the main agent."""
        await self.messages_writer.write({
            "session_id": self.session_id,
            "source": "agent",
            "target": "user",
            "message_type": "agent_response",
            "content": message.get("content", ""),
            "metadata": json.dumps({
                "project_id": self.project_id,
                "from_agent": message.get("sender_id", ""),
            }),
        })
        logger.info(f"ManagerAgent {self.agent_id} delivered final result")

    async def _handle_worker_error(self, message: dict[str, Any]) -> None:
        """Handle an unrecoverable error from a worker agent."""
        error_text = f"Multi-agent project failed: {message.get('content', 'unknown error')}"
        logger.error(f"Project {self.project_id} worker error: {error_text}")
        await self.messages_writer.write({
            "session_id": self.session_id,
            "source": "agent",
            "target": "user",
            "message_type": "agent_response",
            "content": error_text,
        })
        await self._update_project_status("failed")
        self._running = False

    async def _forward_status(self, message: dict[str, Any]) -> None:
        """Forward progress status to the user session."""
        sender = message.get("sender_id", "sub-agent")
        content = message.get("content", "")
        status_text = f"[{sender}] {content}"
        await self.messages_writer.write({
            "session_id": self.session_id,
            "source": "agent",
            "target": "user",
            "message_type": "tool_result",
            "content": json.dumps({"status": status_text}),
        })

    async def _complete_project(self) -> None:
        """Cancel all workers, update project status, stop self."""
        for spec in self.worker_specs:
            await self.kanban_writer.write({
                "project_id": self.project_id,
                "sender_id": self.agent_id,
                "target_id": spec.agent_id,
                "msg_type": "control",
                "content": "cancel",
            })
        await self._update_project_status("completed")
        self._running = False
        logger.info(f"Project {self.project_id} completed")

    async def _update_project_status(self, status: str) -> None:
        """Write a project status update to kanban_projects stream."""
        await self.projects_writer.write({
            "project_id": self.project_id,
            "name": "",
            "description": "",
            "status": status,
            "created_by": "main",
            "session_id": self.session_id,
            "agent_ids": [spec.agent_id for spec in self.worker_specs],
        })
```

### Step 4: Run tests to verify they pass

```bash
pytest tests/test_manager_agent.py -v
```

Expected: All tests PASS.

### Step 5: Run full suite

```bash
pytest -x -q
```

### Step 6: Commit

```bash
git add pulsebot/agents/manager_agent.py tests/test_manager_agent.py
git commit -m "feat: implement ManagerAgent bridging kanban and messages streams"
```

---

## Task 6: ProjectManager

**Files:**
- Create: `pulsebot/agents/project_manager.py`
- Modify: `pulsebot/agents/__init__.py`
- Test: `tests/test_project_manager.py`

### Step 1: Write the failing test

```python
# tests/test_project_manager.py
"""Tests for ProjectManager class."""

from __future__ import annotations

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pulsebot.agents.models import SubAgentSpec


@pytest.fixture
def mock_timeplus():
    client = MagicMock()
    client.host = "localhost"
    client.port = 8463
    client.username = "default"
    client.password = ""
    client.query = MagicMock(return_value=[])
    return client


@pytest.fixture
def mock_config():
    cfg = MagicMock()
    cfg.agent.model = "test-model"
    cfg.agent.provider = "anthropic"
    cfg.agent.temperature = 0.7
    cfg.agent.max_tokens = 4096
    cfg.multi_agent.max_agents_per_project = 10
    cfg.multi_agent.max_concurrent_projects = 5
    return cfg


@pytest.fixture
def worker_specs():
    return [
        SubAgentSpec(
            name="Researcher",
            task_description="Research things",
            project_id="",  # set by ProjectManager
            target_agents=[],
        ),
    ]


def make_project_manager(mock_timeplus, mock_config):
    mock_llm = MagicMock()
    mock_skill_loader = MagicMock()
    mock_skill_loader.get_loaded_skills = MagicMock(return_value=[])
    mock_skill_loader.create_subset = MagicMock(return_value=MagicMock(
        get_tools=MagicMock(return_value=[]),
        get_loaded_skills=MagicMock(return_value=[]),
    ))
    mock_skill_loader.get_tools = MagicMock(return_value=[])
    mock_executor = MagicMock()

    from pulsebot.agents.project_manager import ProjectManager
    with patch("pulsebot.agents.sub_agent.StreamReader"), \
         patch("pulsebot.agents.sub_agent.StreamWriter"), \
         patch("pulsebot.agents.manager_agent.StreamWriter"), \
         patch("pulsebot.agents.project_manager.StreamWriter"):
        return ProjectManager(
            config=mock_config,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            skill_loader=mock_skill_loader,
            executor=mock_executor,
        )


@pytest.mark.asyncio
async def test_create_project_returns_project_id(
        mock_timeplus, mock_config, worker_specs):
    pm = make_project_manager(mock_timeplus, mock_config)

    with patch("pulsebot.agents.project_manager.ManagerAgent") as MockManager, \
         patch("pulsebot.agents.project_manager.SubAgent") as MockSubAgent, \
         patch("asyncio.create_task") as mock_create_task:
        MockManager.return_value.run = AsyncMock()
        MockSubAgent.return_value.run = AsyncMock()
        mock_create_task.return_value = MagicMock()
        pm._kanban_writer.write = AsyncMock()
        pm._projects_writer.write = AsyncMock()
        pm._agents_writer.write = AsyncMock()

        project_id = await pm.create_project(
            name="Test Project",
            description="A test",
            agents=worker_specs,
            session_id="sess_001",
            initial_messages=[],
        )

        assert project_id.startswith("proj_")
        assert len(project_id) > 5


@pytest.mark.asyncio
async def test_create_project_sets_project_id_on_specs(
        mock_timeplus, mock_config, worker_specs):
    pm = make_project_manager(mock_timeplus, mock_config)

    with patch("pulsebot.agents.project_manager.ManagerAgent") as MockManager, \
         patch("pulsebot.agents.project_manager.SubAgent") as MockSubAgent, \
         patch("asyncio.create_task"):
        MockManager.return_value.run = AsyncMock()
        MockSubAgent.return_value.run = AsyncMock()
        pm._kanban_writer.write = AsyncMock()
        pm._projects_writer.write = AsyncMock()
        pm._agents_writer.write = AsyncMock()

        project_id = await pm.create_project(
            name="Test Project",
            description="A test",
            agents=worker_specs,
            session_id="sess_001",
            initial_messages=[],
        )

        for spec in worker_specs:
            assert spec.project_id == project_id


@pytest.mark.asyncio
async def test_list_projects_empty_initially(mock_timeplus, mock_config):
    pm = make_project_manager(mock_timeplus, mock_config)
    projects = pm.list_projects()
    assert projects == []


@pytest.mark.asyncio
async def test_get_project_status_returns_none_for_unknown(
        mock_timeplus, mock_config):
    pm = make_project_manager(mock_timeplus, mock_config)
    status = pm.get_project_status("proj_nonexistent")
    assert status is None


@pytest.mark.asyncio
async def test_cancel_project_sends_control_messages(
        mock_timeplus, mock_config, worker_specs):
    pm = make_project_manager(mock_timeplus, mock_config)

    with patch("pulsebot.agents.project_manager.ManagerAgent") as MockManager, \
         patch("pulsebot.agents.project_manager.SubAgent") as MockSubAgent, \
         patch("asyncio.create_task") as mock_task:
        mock_task_handle = MagicMock()
        mock_task.return_value = mock_task_handle
        MockManager.return_value.run = AsyncMock()
        MockSubAgent.return_value.run = AsyncMock()
        pm._kanban_writer.write = AsyncMock()
        pm._projects_writer.write = AsyncMock()
        pm._agents_writer.write = AsyncMock()

        project_id = await pm.create_project(
            name="Test", description="test",
            agents=worker_specs, session_id="sess_001",
            initial_messages=[],
        )

        await pm.cancel_project(project_id)

        # Tasks should have been cancelled
        mock_task_handle.cancel.assert_called()
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_project_manager.py -v
```

Expected: `ModuleNotFoundError: No module named 'pulsebot.agents.project_manager'`

### Step 3: Implement ProjectManager

```python
# pulsebot/agents/project_manager.py
"""ProjectManager: creates, monitors, and cancels multi-agent projects."""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import TYPE_CHECKING, Any

from pulsebot.agents.manager_agent import ManagerAgent
from pulsebot.agents.models import ProjectState, SubAgentSpec
from pulsebot.agents.sub_agent import SubAgent
from pulsebot.timeplus.streams import StreamWriter
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.config import Config
    from pulsebot.core.executor import ToolExecutor
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


class ProjectManager:
    """
    Manages the lifecycle of multi-agent projects.

    Provides create/cancel/status operations used by the project_manager skill.
    Each project spawns a ManagerAgent + worker SubAgents as asyncio tasks.
    """

    def __init__(
        self,
        config: "Config",
        timeplus: "TimeplusClient",
        llm_provider: "LLMProvider",
        skill_loader: "SkillLoader",
        executor: "ToolExecutor",
    ) -> None:
        from pulsebot.timeplus.client import TimeplusClient

        self.config = config
        self.timeplus = timeplus
        self.llm = llm_provider
        self.skills = skill_loader
        self.executor = executor

        self._projects: dict[str, ProjectState] = {}
        self._agent_tasks: dict[str, asyncio.Task] = {}

        # Dedicated batch client for metadata writes
        _batch = TimeplusClient(
            host=timeplus.host,
            port=timeplus.port,
            username=timeplus.username,
            password=timeplus.password,
        )
        self._kanban_writer = StreamWriter(_batch, "kanban")
        self._projects_writer = StreamWriter(_batch, "kanban_projects")
        self._agents_writer = StreamWriter(_batch, "kanban_agents")

    async def create_project(
        self,
        name: str,
        description: str,
        agents: list[SubAgentSpec],
        session_id: str,
        initial_messages: list[dict[str, Any]] | None = None,
    ) -> str:
        """Create a new project, persist metadata, and spawn all agents.

        Returns:
            The generated project_id.
        """
        max_agents = self.config.multi_agent.max_agents_per_project
        if len(agents) > max_agents:
            raise ValueError(
                f"Too many agents: {len(agents)} > max {max_agents}"
            )
        max_projects = self.config.multi_agent.max_concurrent_projects
        active = sum(1 for p in self._projects.values() if p.status == "active")
        if active >= max_projects:
            raise ValueError(
                f"Too many concurrent projects: {active} >= max {max_projects}"
            )

        project_id = f"proj_{uuid.uuid4().hex[:12]}"
        initial_messages = initial_messages or []

        # Set project_id on all specs
        for spec in agents:
            spec.project_id = project_id

        manager_spec = SubAgentSpec(
            name="Manager",
            agent_id=f"manager_{project_id}",
            role="manager",
            task_description=(
                "You are the project manager. Coordinate worker agents, "
                "collect their results, and deliver the final output."
            ),
            project_id=project_id,
            target_agents=[],
            skills=[],
        )

        # Persist project metadata
        await self._write_project_metadata(
            project_id, name, description, agents, session_id
        )
        # Persist all agent metadata
        for spec in [manager_spec] + agents:
            await self._write_agent_metadata(spec)

        # Track state
        self._projects[project_id] = ProjectState(
            project_id=project_id,
            name=name,
            description=description,
            session_id=session_id,
            agent_ids=[spec.agent_id for spec in agents],
        )

        # Spawn Manager Agent
        manager = ManagerAgent(
            spec=manager_spec,
            worker_specs=agents,
            session_id=session_id,
            timeplus=self.timeplus,
            llm_provider=self.llm,
            skill_loader=self.skills,
            executor=self.executor,
            config=self.config,
            initial_messages=initial_messages,
        )
        self._agent_tasks[manager_spec.agent_id] = asyncio.create_task(
            manager.run(), name=f"manager_{project_id}"
        )

        # Spawn worker sub-agents
        for spec in agents:
            agent = SubAgent(
                spec=spec,
                timeplus=self.timeplus,
                llm_provider=self.llm,
                skill_loader=self.skills,
                executor=self.executor,
                config=self.config,
            )
            self._agent_tasks[spec.agent_id] = asyncio.create_task(
                agent.run(), name=spec.agent_id
            )

        logger.info(
            f"Project {project_id} created with {len(agents)} worker(s)",
            extra={"project_id": project_id, "session_id": session_id},
        )
        return project_id

    def list_projects(self, status: str | None = None) -> list[dict[str, Any]]:
        """Return summary dicts for all tracked projects.

        Args:
            status: Optional filter ('active', 'completed', 'failed', 'cancelled').
        """
        result = []
        for state in self._projects.values():
            if status is None or state.status == status:
                result.append({
                    "project_id": state.project_id,
                    "name": state.name,
                    "description": state.description,
                    "status": state.status,
                    "agent_count": len(state.agent_ids),
                    "session_id": state.session_id,
                })
        return result

    def get_project_status(self, project_id: str) -> dict[str, Any] | None:
        """Return detailed status for a specific project, or None if not found."""
        state = self._projects.get(project_id)
        if state is None:
            return None
        return {
            "project_id": state.project_id,
            "name": state.name,
            "description": state.description,
            "status": state.status,
            "agent_ids": state.agent_ids,
            "session_id": state.session_id,
        }

    async def cancel_project(self, project_id: str) -> bool:
        """Cancel a running project.

        Cancels all asyncio tasks for the project.

        Returns:
            True if project was found and cancelled.
        """
        state = self._projects.get(project_id)
        if state is None:
            return False

        all_ids = [f"manager_{project_id}"] + state.agent_ids
        for agent_id in all_ids:
            task = self._agent_tasks.pop(agent_id, None)
            if task and not task.done():
                task.cancel()

        state.status = "cancelled"
        logger.info(f"Project {project_id} cancelled")
        return True

    async def _write_project_metadata(
        self,
        project_id: str,
        name: str,
        description: str,
        agents: list[SubAgentSpec],
        session_id: str,
    ) -> None:
        await self._projects_writer.write({
            "project_id": project_id,
            "name": name,
            "description": description,
            "status": "active",
            "created_by": "main",
            "session_id": session_id,
            "agent_ids": [s.agent_id for s in agents],
        })

    async def _write_agent_metadata(self, spec: SubAgentSpec) -> None:
        await self._agents_writer.write({
            "agent_id": spec.agent_id,
            "project_id": spec.project_id,
            "name": spec.name,
            "role": spec.role,
            "task_description": spec.task_description,
            "target_agents": spec.target_agents,
            "status": "pending",
            "skills": spec.skills or [],
            "skill_overrides": json.dumps(spec.skill_overrides or {}),
            "config": json.dumps({
                "model": spec.model,
                "provider": spec.provider,
                "temperature": spec.temperature,
                "max_tokens": spec.max_tokens,
                "max_iterations": spec.max_iterations,
                "enable_memory": spec.enable_memory,
            }),
            "checkpoint_sn": 0,
        })
```

Update `pulsebot/agents/__init__.py`:

```python
"""Multi-agent coordination module for PulseBot."""

from pulsebot.agents.models import ProjectState, SubAgentSpec
from pulsebot.agents.project_manager import ProjectManager

__all__ = ["SubAgentSpec", "ProjectState", "ProjectManager"]
```

### Step 4: Run tests to verify they pass

```bash
pytest tests/test_project_manager.py -v
```

Expected: All tests PASS.

### Step 5: Run full suite

```bash
pytest -x -q
```

### Step 6: Commit

```bash
git add pulsebot/agents/project_manager.py pulsebot/agents/__init__.py tests/test_project_manager.py
git commit -m "feat: implement ProjectManager with asyncio task spawning"
```

---

## Task 7: Ensure Kanban Streams Created on Startup

The `SubAgent` connects to kanban on startup. Streams must exist. The existing pattern in `agent.py` calls `_ensure_streams_exist()` — we need kanban DDLs included there.

**Files:**
- Modify: `pulsebot/core/agent.py` — add kanban stream DDLs to `_ensure_streams_exist()`

> Note: This is the ONLY change to agent.py, and it is purely additive (no behavior change to the main loop).

### Step 1: Read current _ensure_streams_exist

Lines ~198–230 of `pulsebot/core/agent.py` (already read above).

### Step 2: Modify _ensure_streams_exist to include kanban streams

In `pulsebot/core/agent.py`, update the `_ensure_streams_exist` method to add the three kanban DDLs:

```python
async def _ensure_streams_exist(self) -> None:
    """Ensure all required Timeplus streams exist."""
    from pulsebot.timeplus.setup import (
        create_database,
        MESSAGES_STREAM_DDL,
        LLM_LOGS_STREAM_DDL,
        TOOL_LOGS_STREAM_DDL,
        EVENTS_STREAM_DDL,
        KANBAN_STREAM_DDL,
        KANBAN_PROJECTS_STREAM_DDL,
        KANBAN_AGENTS_STREAM_DDL,
    )

    logger.info("Ensuring required streams exist...")
    await create_database(self.tp)

    streams = [
        ("messages", MESSAGES_STREAM_DDL),
        ("llm_logs", LLM_LOGS_STREAM_DDL),
        ("tool_logs", TOOL_LOGS_STREAM_DDL),
        ("events", EVENTS_STREAM_DDL),
        ("kanban", KANBAN_STREAM_DDL),
        ("kanban_projects", KANBAN_PROJECTS_STREAM_DDL),
        ("kanban_agents", KANBAN_AGENTS_STREAM_DDL),
    ]

    for name, ddl in streams:
        try:
            self.tp.execute(ddl)
            logger.debug(f"Ensured stream exists: {name}")
        except Exception as e:
            logger.warning(f"Could not create stream {name}: {e}")
```

### Step 3: Run existing tests to verify no regressions

```bash
pytest -x -q
```

Expected: All tests pass (no behavior change — DDLs use `IF NOT EXISTS`).

### Step 4: Commit

```bash
git add pulsebot/core/agent.py
git commit -m "feat: ensure kanban streams created on agent startup"
```

---

## Task 8: project_manager Built-in Skill

**Files:**
- Create: `pulsebot/skills/builtin/project_manager.py`
- Modify: `pulsebot/skills/loader.py` (add to `BUILTIN_SKILLS`)
- Modify: `pulsebot/factory.py` (special registration)
- Test: `tests/test_project_manager_skill.py`

### Step 1: Write the failing test

```python
# tests/test_project_manager_skill.py
"""Tests for the project_manager built-in skill."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_pm():
    pm = MagicMock()
    pm.create_project = AsyncMock(return_value="proj_abc123")
    pm.list_projects = MagicMock(return_value=[
        {"project_id": "proj_abc123", "name": "Test", "status": "active"}
    ])
    pm.cancel_project = AsyncMock(return_value=True)
    pm.get_project_status = MagicMock(return_value={
        "project_id": "proj_abc123", "status": "active"
    })
    return pm


@pytest.fixture
def skill(mock_pm):
    from pulsebot.skills.builtin.project_manager import ProjectManagerSkill
    return ProjectManagerSkill(project_manager=mock_pm)


def test_project_manager_skill_has_required_tools(skill):
    tool_names = {t.name for t in skill.get_tools()}
    assert "create_project" in tool_names
    assert "list_projects" in tool_names
    assert "cancel_project" in tool_names
    assert "get_project_status" in tool_names


@pytest.mark.asyncio
async def test_create_project_tool_calls_project_manager(skill, mock_pm):
    result = await skill.execute("create_project", {
        "name": "Market Research",
        "description": "Research AI market",
        "agents": [
            {
                "name": "Researcher",
                "task_description": "Research things",
                "target_agents": [],
            }
        ],
        "session_id": "sess_001",
        "initial_messages": [],
    })
    assert result.success is True
    assert "proj_abc123" in result.output
    mock_pm.create_project.assert_called_once()


@pytest.mark.asyncio
async def test_list_projects_tool(skill, mock_pm):
    result = await skill.execute("list_projects", {})
    assert result.success is True
    assert "proj_abc123" in result.output


@pytest.mark.asyncio
async def test_cancel_project_tool(skill, mock_pm):
    result = await skill.execute("cancel_project", {"project_id": "proj_abc123"})
    assert result.success is True
    mock_pm.cancel_project.assert_called_once_with("proj_abc123")


@pytest.mark.asyncio
async def test_get_project_status_tool(skill, mock_pm):
    result = await skill.execute("get_project_status", {"project_id": "proj_abc123"})
    assert result.success is True
    assert "proj_abc123" in result.output


@pytest.mark.asyncio
async def test_unknown_tool_returns_failure(skill):
    result = await skill.execute("nonexistent_tool", {})
    assert result.success is False
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_project_manager_skill.py -v
```

Expected: `ModuleNotFoundError: No module named 'pulsebot.skills.builtin.project_manager'`

### Step 3: Implement the skill

```python
# pulsebot/skills/builtin/project_manager.py
"""Built-in skill for creating and managing multi-agent projects."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult

if TYPE_CHECKING:
    from pulsebot.agents.project_manager import ProjectManager


class ProjectManagerSkill(BaseSkill):
    """Skill that exposes multi-agent project management tools to the main agent."""

    name = "project_manager"
    description = "Create and manage multi-agent projects that decompose complex tasks"

    def __init__(self, project_manager: "ProjectManager") -> None:
        self._pm = project_manager

    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="create_project",
                description=(
                    "Create a new multi-agent project. Spawns a manager agent "
                    "and worker sub-agents that collaborate via a kanban stream. "
                    "Use for complex tasks that benefit from parallel or sequential "
                    "decomposition (research + analysis + writing, etc.)."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Short human-readable project name",
                        },
                        "description": {
                            "type": "string",
                            "description": "What this project aims to accomplish",
                        },
                        "agents": {
                            "type": "array",
                            "description": "Worker agent specifications",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Agent name (used to derive agent_id)"},
                                    "task_description": {"type": "string", "description": "System-level role instructions"},
                                    "target_agents": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Agent IDs that receive this agent's output. Empty = send to manager.",
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Skill names to load. Omit to inherit all main agent skills.",
                                    },
                                    "model": {"type": "string", "description": "Override LLM model"},
                                    "provider": {"type": "string", "description": "Override LLM provider"},
                                },
                                "required": ["name", "task_description", "target_agents"],
                            },
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Current user session ID (for routing final result back to user)",
                        },
                        "initial_messages": {
                            "type": "array",
                            "description": "Initial task messages dispatched by the manager",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string", "description": "Agent ID to send task to"},
                                    "content": {"type": "string", "description": "Task content"},
                                },
                                "required": ["target", "content"],
                            },
                        },
                    },
                    "required": ["name", "description", "agents", "session_id"],
                },
            ),
            ToolDefinition(
                name="list_projects",
                description="List all active and recent multi-agent projects.",
                parameters={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["active", "completed", "failed", "cancelled"],
                            "description": "Filter by status. Omit to list all.",
                        },
                    },
                },
            ),
            ToolDefinition(
                name="cancel_project",
                description="Cancel a running multi-agent project and stop all its agents.",
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID to cancel"},
                    },
                    "required": ["project_id"],
                },
            ),
            ToolDefinition(
                name="get_project_status",
                description="Get detailed status of a specific project including all agent states.",
                parameters={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project ID"},
                    },
                    "required": ["project_id"],
                },
            ),
        ]

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        try:
            if tool_name == "create_project":
                return await self._create_project(arguments)
            elif tool_name == "list_projects":
                return self._list_projects(arguments)
            elif tool_name == "cancel_project":
                return await self._cancel_project(arguments)
            elif tool_name == "get_project_status":
                return self._get_project_status(arguments)
            else:
                return ToolResult.fail(f"Unknown tool: {tool_name}")
        except Exception as e:
            return ToolResult.fail(str(e))

    async def _create_project(self, args: dict) -> ToolResult:
        from pulsebot.agents.models import SubAgentSpec

        raw_agents = args.get("agents", [])
        specs = [
            SubAgentSpec(
                name=a["name"],
                task_description=a["task_description"],
                project_id="",  # set by ProjectManager
                target_agents=a.get("target_agents", []),
                skills=a.get("skills"),
                model=a.get("model"),
                provider=a.get("provider"),
            )
            for a in raw_agents
        ]

        project_id = await self._pm.create_project(
            name=args["name"],
            description=args["description"],
            agents=specs,
            session_id=args["session_id"],
            initial_messages=args.get("initial_messages", []),
        )
        return ToolResult.ok(
            f"Project created: {project_id}\n"
            f"Spawned {len(specs)} worker agent(s). "
            f"The manager agent will deliver results to your session."
        )

    def _list_projects(self, args: dict) -> ToolResult:
        status_filter = args.get("status")
        projects = self._pm.list_projects(status=status_filter)
        if not projects:
            return ToolResult.ok("No projects found.")
        lines = ["Projects:"]
        for p in projects:
            lines.append(
                f"  [{p['status']}] {p['project_id']} — {p['name']} "
                f"({p['agent_count']} agents)"
            )
        return ToolResult.ok("\n".join(lines))

    async def _cancel_project(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        cancelled = await self._pm.cancel_project(project_id)
        if cancelled:
            return ToolResult.ok(f"Project {project_id} cancelled.")
        return ToolResult.fail(f"Project {project_id} not found.")

    def _get_project_status(self, args: dict) -> ToolResult:
        project_id = args["project_id"]
        status = self._pm.get_project_status(project_id)
        if status is None:
            return ToolResult.fail(f"Project {project_id} not found.")
        return ToolResult.ok(json.dumps(status, indent=2))
```

### Step 4: Register in BUILTIN_SKILLS

In `pulsebot/skills/loader.py`, add `project_manager` to the registry:

```python
BUILTIN_SKILLS = {
    "web_search": "pulsebot.skills.builtin.web_search.WebSearchSkill",
    "file_ops": "pulsebot.skills.builtin.file_ops.FileOpsSkill",
    "shell": "pulsebot.skills.builtin.shell.ShellSkill",
    "workspace": "pulsebot.skills.builtin.workspace.WorkspaceSkill",
    "scheduler": "pulsebot.skills.builtin.scheduler.SchedulerSkill",
    "project_manager": "pulsebot.skills.builtin.project_manager.ProjectManagerSkill",
}
```

### Step 5: Run tests to verify they pass

```bash
pytest tests/test_project_manager_skill.py -v
```

Expected: All tests PASS.

### Step 6: Run full suite

```bash
pytest -x -q
```

### Step 7: Commit

```bash
git add pulsebot/skills/builtin/project_manager.py pulsebot/skills/loader.py tests/test_project_manager_skill.py
git commit -m "feat: add project_manager built-in skill"
```

---

## Task 9: Factory Integration

Wire up `ProjectManagerSkill` in `factory.py` using the same "special registration" pattern as `WorkspaceSkill`, `SchedulerSkill`, and `SkillManagerSkill`.

**Files:**
- Modify: `pulsebot/factory.py`
- Test: `tests/test_factory_integration.py`

### Step 1: Write the failing test

```python
# tests/test_factory_integration.py
"""Tests for factory.py project_manager skill integration."""

import pytest
from unittest.mock import MagicMock, patch

from pulsebot.config import Config, MultiAgentConfig


def test_create_skill_loader_registers_project_manager_when_configured():
    """When 'project_manager' is in skills.builtin, it should be registered."""
    config = Config()
    config.skills.builtin = ["project_manager"]
    config.multi_agent = MultiAgentConfig()

    mock_timeplus = MagicMock()
    mock_timeplus.host = "localhost"
    mock_timeplus.port = 8463
    mock_timeplus.username = "default"
    mock_timeplus.password = ""

    mock_llm = MagicMock()
    mock_executor = MagicMock()

    with patch("pulsebot.timeplus.client.TimeplusClient") as MockClient:
        MockClient.return_value = mock_timeplus
        MockClient.from_config.return_value = mock_timeplus

        from pulsebot.factory import create_skill_loader
        loader = create_skill_loader(
            config,
            timeplus=mock_timeplus,
            llm_provider=mock_llm,
            executor=mock_executor,
        )

    skill = loader.get_skill("project_manager")
    assert skill is not None
    assert skill.name == "project_manager"
    tool_names = {t.name for t in skill.get_tools()}
    assert "create_project" in tool_names


def test_create_skill_loader_without_project_manager():
    """Without project_manager in builtin list, skill should not be loaded."""
    config = Config()
    config.skills.builtin = ["file_ops"]

    from pulsebot.factory import create_skill_loader
    loader = create_skill_loader(config)

    skill = loader.get_skill("project_manager")
    assert skill is None
```

### Step 2: Run test to verify it fails

```bash
pytest tests/test_factory_integration.py -v
```

Expected: First test fails — `create_skill_loader` doesn't accept `timeplus`, `llm_provider`, `executor` kwargs yet (or project_manager skill is not registered).

### Step 3: Update factory.py

Update `create_skill_loader` in `pulsebot/factory.py`:

1. Add `project_manager` to `_SPECIAL`:
```python
_SPECIAL = {"workspace", "scheduler", "skill_manager", "project_manager"}
```

2. Add `timeplus`, `llm_provider`, `executor` optional kwargs:
```python
def create_skill_loader(
    config: "Config",
    timeplus: "TimeplusClient | None" = None,
    llm_provider: "LLMProvider | None" = None,
    executor: "ToolExecutor | None" = None,
) -> "SkillLoader":
```

3. Add project_manager registration block (after skill_manager block):
```python
    # Register ProjectManagerSkill — needs ProjectManager (timeplus + llm + executor)
    if "project_manager" in config.skills.builtin:
        if timeplus is None or llm_provider is None or executor is None:
            _log.warning(
                "project_manager skill requires timeplus, llm_provider, and executor; skipping"
            )
        else:
            from pulsebot.agents.project_manager import ProjectManager
            from pulsebot.skills.builtin.project_manager import ProjectManagerSkill

            pm = ProjectManager(
                config=config,
                timeplus=timeplus,
                llm_provider=llm_provider,
                skill_loader=loader,
                executor=executor,
            )
            skill = ProjectManagerSkill(project_manager=pm)
            loader._skills["project_manager"] = skill
            for tool in skill.get_tools():
                loader._tool_to_skill[tool.name] = "project_manager"

            _log.info(
                "ProjectManager skill registered",
                extra={"tools": [t.name for t in skill.get_tools()]},
            )
```

### Step 4: Update cli.py call site to pass new kwargs

In `pulsebot/cli.py`, find where `create_skill_loader` is called and update to pass `timeplus`, `llm_provider`, and `executor` if available. Look for the agent initialization sequence.

The typical pattern in `cli.py` is:
```python
provider = create_provider(config)
skill_loader = create_skill_loader(config)
executor = create_executor(config, skill_loader)
```

Update to:
```python
provider = create_provider(config)
# Temporary loader without project_manager (executor not yet built)
skill_loader = create_skill_loader(config)
executor = create_executor(config, skill_loader)
# Re-register project_manager skill now that executor is available
if "project_manager" in config.skills.builtin:
    skill_loader = create_skill_loader(
        config,
        timeplus=timeplus_client,
        llm_provider=provider,
        executor=executor,
    )
    executor = create_executor(config, skill_loader)
```

> **Note**: Read `cli.py` first to find the exact location and adapt accordingly. The pattern above is illustrative.

### Step 5: Run tests to verify they pass

```bash
pytest tests/test_factory_integration.py -v
```

Expected: All tests PASS.

### Step 6: Run full suite

```bash
pytest -x -q
```

Expected: All tests PASS. No regressions.

### Step 7: Commit

```bash
git add pulsebot/factory.py pulsebot/cli.py tests/test_factory_integration.py
git commit -m "feat: wire up project_manager skill in factory with ProjectManager injection"
```

---

## Final Verification

### Run linter

```bash
ruff check pulsebot/agents/ pulsebot/skills/builtin/project_manager.py
```

Fix any issues, then:

```bash
ruff check . --fix
```

### Run full test suite

```bash
pytest -v --tb=short
```

Expected: All tests pass.

### Verify imports work end-to-end

```bash
python -c "
from pulsebot.agents import SubAgentSpec, ProjectState, ProjectManager
from pulsebot.agents.sub_agent import SubAgent
from pulsebot.agents.manager_agent import ManagerAgent
from pulsebot.skills.builtin.project_manager import ProjectManagerSkill
from pulsebot.timeplus.setup import KANBAN_STREAM_DDL, KANBAN_PROJECTS_STREAM_DDL, KANBAN_AGENTS_STREAM_DDL
from pulsebot.config import Config, MultiAgentConfig
print('All imports OK')
"
```

### Final commit (if any cleanup)

```bash
git add -p  # review and stage any final fixes
git commit -m "chore: final cleanup for multi-agent support phases 1-2"
```

---

## Files Created/Modified Summary

| File | Change |
|------|--------|
| `pulsebot/timeplus/setup.py` | Add 3 kanban DDL constants |
| `pulsebot/config.py` | Add `MultiAgentConfig`, add to `Config` |
| `pulsebot/agents/__init__.py` | **New** |
| `pulsebot/agents/models.py` | **New** — `SubAgentSpec`, `ProjectState` |
| `pulsebot/agents/sub_agent.py` | **New** — `SubAgent` |
| `pulsebot/agents/manager_agent.py` | **New** — `ManagerAgent` |
| `pulsebot/agents/project_manager.py` | **New** — `ProjectManager` |
| `pulsebot/skills/loader.py` | Add `get_loaded_skills()`, `create_subset()`, register `project_manager` |
| `pulsebot/skills/builtin/project_manager.py` | **New** — `ProjectManagerSkill` |
| `pulsebot/factory.py` | Register `project_manager` skill with `ProjectManager` injection |
| `pulsebot/core/agent.py` | Add kanban DDL imports to `_ensure_streams_exist()` |
| `pulsebot/cli.py` | Pass `timeplus`, `llm_provider`, `executor` to `create_skill_loader` |
| `tests/test_multi_agent_setup.py` | **New** |
| `tests/test_multi_agent_models.py` | **New** |
| `tests/test_skill_loader_extensions.py` | **New** |
| `tests/test_sub_agent.py` | **New** |
| `tests/test_manager_agent.py` | **New** |
| `tests/test_project_manager.py` | **New** |
| `tests/test_project_manager_skill.py` | **New** |
| `tests/test_factory_integration.py` | **New** |
