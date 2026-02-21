"""WorkspaceManager — agent-side workspace state and subprocess management.

Owns:
  - On-disk directory layout for every session / task
  - task_id slug generation and collision resolution
  - In-memory task registry (session_id → task_id → TaskState)
  - Backend subprocess spawning, tracking, and termination
  - pip dependency installation

This module runs exclusively on the agent. The API server never imports it.

Directory layout
----------------
  {base_dir}/
    {session_id}/
      {task_id}/
        index.html        ← frontend (apps)
        backend.py        ← FastAPI backend (fullstack only)
        requirements.txt  ← optional pip deps
        backend.log       ← backend stdout + stderr
        <any other files> ← static artifacts
"""

from __future__ import annotations

import asyncio
import os
import re
import shutil
import socket
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pulsebot.utils import get_logger
from pulsebot.workspace.config import WorkspaceConfig

logger = get_logger(__name__)


# ── helpers ───────────────────────────────────────────────────────────────────

def _find_free_port() -> int:
    """Ask the OS for an available TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def _slugify(text: str, max_length: int = 40) -> str:
    """Convert a human-readable name into a URL-safe slug.

    Examples:
        "CPU Monitor App"   → "cpu-monitor-app"
        "Q3 Sales Report!"  → "q3-sales-report"
        "  Hello   World  " → "hello-world"
    """
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug[:max_length] or "task"


def _tail(path: Path, n: int = 30) -> str:
    """Return the last n lines of a text file."""
    try:
        return "\n".join(path.read_text(errors="replace").splitlines()[-n:])
    except Exception:
        return "(log unavailable)"


# ── data model ────────────────────────────────────────────────────────────────

@dataclass
class TaskState:
    """Runtime state for one workspace task."""

    session_id: str
    task_id: str
    task_name: str
    artifact_type: str                        # "file" | "html_app" | "fullstack_app"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    process: asyncio.subprocess.Process | None = None
    backend_port: int | None = None

    @property
    def is_running(self) -> bool:
        return self.process is not None and self.process.returncode is None

    @property
    def status(self) -> str:
        if self.artifact_type == "fullstack_app":
            return "running" if self.is_running else "stopped"
        return "ready"

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "task_id": self.task_id,
            "task_name": self.task_name,
            "artifact_type": self.artifact_type,
            "status": self.status,
            "backend_port": self.backend_port,
            "created_at": self.created_at.isoformat(),
        }


# ── manager ───────────────────────────────────────────────────────────────────

class WorkspaceManager:
    """Manages workspace directories and backend subprocesses on the agent.

    Example::

        mgr = WorkspaceManager(cfg)
        task_id = mgr.create_task("abc-123", "CPU Monitor", "fullstack_app")
        mgr.write_task_file("abc-123", task_id, "index.html", html_str)
        port = await mgr.start_backend("abc-123", task_id)
    """

    def __init__(self, config: WorkspaceConfig) -> None:
        self._cfg = config
        self._base = Path(config.base_dir).resolve()
        # session_id → task_id → TaskState
        self._registry: dict[str, dict[str, TaskState]] = {}

    # ── directory helpers ─────────────────────────────────────────────────

    def task_dir(self, session_id: str, task_id: str) -> Path:
        """Absolute path to a task directory (not auto-created)."""
        return self._base / session_id / task_id

    def _ensure_task_dir(self, session_id: str, task_id: str) -> Path:
        d = self.task_dir(session_id, task_id)
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ── slug / task creation ──────────────────────────────────────────────

    def _unique_slug(self, session_id: str, task_name: str) -> str:
        """Derive a unique task_id slug for this session.

        Appends -2, -3 … if the base slug already exists.
        """
        base = _slugify(task_name)
        existing = set(self._registry.get(session_id, {}).keys())
        # Also check disk in case manager was restarted
        session_dir = self._base / session_id
        if session_dir.exists():
            existing |= {p.name for p in session_dir.iterdir() if p.is_dir()}

        slug = base
        counter = 2
        while slug in existing:
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    def create_task(
        self,
        session_id: str,
        task_name: str,
        artifact_type: str,
    ) -> str:
        """Register a new task and create its directory.

        Args:
            session_id: Conversation session ID.
            task_name: Human-readable name (will be slugified).
            artifact_type: One of "file", "html_app", "fullstack_app".

        Returns:
            The generated task_id slug.
        """
        task_id = self._unique_slug(session_id, task_name)
        self._ensure_task_dir(session_id, task_id)

        state = TaskState(
            session_id=session_id,
            task_id=task_id,
            task_name=task_name,
            artifact_type=artifact_type,
        )
        self._registry.setdefault(session_id, {})[task_id] = state
        logger.info(f"[workspace] created task session={session_id} task={task_id} type={artifact_type}")
        return task_id

    # ── file I/O ──────────────────────────────────────────────────────────

    def write_task_file(
        self,
        session_id: str,
        task_id: str,
        filename: str,
        content: str,
    ) -> Path:
        """Write a file into a task directory with path-traversal protection.

        Args:
            session_id: Session identifier.
            task_id: Task identifier.
            filename: Filename or relative sub-path within the task dir.
            content: Text content to write.

        Returns:
            Absolute path to the written file.

        Raises:
            ValueError: If the resolved path escapes the task directory.
        """
        task_d = self._ensure_task_dir(session_id, task_id)
        dest = (task_d / filename).resolve()
        if not str(dest).startswith(str(task_d)):
            raise ValueError(f"Path traversal blocked: {filename}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
        logger.debug(f"[workspace] wrote {filename} → {dest}")
        return dest

    def resolve_task_file(
        self,
        session_id: str,
        task_id: str,
        relative_path: str,
    ) -> Path | None:
        """Safely resolve a file path within a task directory.

        Returns the absolute Path if it exists and is within bounds, else None.
        """
        task_d = self.task_dir(session_id, task_id)
        if not task_d.exists():
            return None
        target = (task_d / relative_path).resolve()
        if not str(target).startswith(str(task_d)):
            return None
        return target if target.is_file() else None

    # ── task listing ──────────────────────────────────────────────────────

    def list_tasks(self, session_id: str) -> list[dict[str, Any]]:
        """Return metadata for all tasks in a session."""
        tasks = []
        for task_id, state in self._registry.get(session_id, {}).items():
            tasks.append(state.to_dict())

        # Also surface tasks that exist on disk but not in memory registry
        # (e.g. after a manager restart)
        session_dir = self._base / session_id
        if session_dir.exists():
            known = set(self._registry.get(session_id, {}).keys())
            for d in sorted(session_dir.iterdir()):
                if d.is_dir() and d.name not in known:
                    tasks.append({
                        "session_id": session_id,
                        "task_id": d.name,
                        "task_name": d.name,
                        "artifact_type": "unknown",
                        "status": "unknown",
                        "backend_port": None,
                        "created_at": None,
                    })
        return tasks

    def get_task(self, session_id: str, task_id: str) -> TaskState | None:
        """Return TaskState for a specific task, or None."""
        return self._registry.get(session_id, {}).get(task_id)

    # ── backend subprocess lifecycle ──────────────────────────────────────

    async def start_backend(self, session_id: str, task_id: str) -> int:
        """Launch (or restart) the backend.py for a task.

        The backend.py must read PORT from os.environ and start uvicorn
        bound to 127.0.0.1 on that port.

        Args:
            session_id: Session identifier.
            task_id: Task identifier.

        Returns:
            The TCP port the backend is now listening on.

        Raises:
            FileNotFoundError: backend.py does not exist.
            RuntimeError: Process exited immediately on start.
        """
        task_d = self.task_dir(session_id, task_id)
        backend_path = task_d / "backend.py"
        if not backend_path.exists():
            raise FileNotFoundError(
                f"No backend.py in task {session_id}/{task_id}"
            )

        # Stop any existing process first
        await self.stop_backend(session_id, task_id)

        # Install requirements if present
        await self._install_requirements(task_d)

        port = _find_free_port()
        log_path = task_d / "backend.log"

        process = await asyncio.create_subprocess_exec(
            sys.executable,
            str(backend_path),
            env={
                **os.environ,
                "PORT": str(port),
                "SESSION_ID": session_id,
                "TASK_ID": task_id,
            },
            cwd=str(task_d),
            stdout=open(log_path, "w"),
            stderr=asyncio.subprocess.STDOUT,
        )

        # Give the process time to bind its port
        await asyncio.sleep(self._cfg.backend_boot_timeout)

        if process.returncode is not None:
            raise RuntimeError(
                f"Backend for {session_id}/{task_id} exited immediately "
                f"(code {process.returncode}).\n"
                f"Log:\n{_tail(log_path)}"
            )

        # Update registry
        state = self._registry.get(session_id, {}).get(task_id)
        if state is None:
            # Task was created before manager restart — reconstruct minimal state
            state = TaskState(
                session_id=session_id,
                task_id=task_id,
                task_name=task_id,
                artifact_type="fullstack_app",
            )
            self._registry.setdefault(session_id, {})[task_id] = state

        state.process = process
        state.backend_port = port

        logger.info(
            f"[workspace] backend started session={session_id} task={task_id} "
            f"pid={process.pid} port={port}"
        )
        return port

    async def stop_backend(self, session_id: str, task_id: str) -> None:
        """Stop the running backend for a task (no-op if not running)."""
        state = self._registry.get(session_id, {}).get(task_id)
        if state is None or not state.is_running:
            return

        state.process.terminate()
        try:
            await asyncio.wait_for(state.process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning(f"[workspace] backend {session_id}/{task_id} did not exit — killing")
            state.process.kill()
            await state.process.wait()

        logger.info(f"[workspace] backend stopped session={session_id} task={task_id}")
        state.process = None
        state.backend_port = None

    def get_backend_port(self, session_id: str, task_id: str) -> int | None:
        """Return the live backend port for a task, or None."""
        state = self._registry.get(session_id, {}).get(task_id)
        return state.backend_port if state and state.is_running else None

    # ── task deletion ─────────────────────────────────────────────────────

    async def delete_task(self, session_id: str, task_id: str) -> None:
        """Stop backend, delete task directory, remove from registry.

        Args:
            session_id: Session identifier.
            task_id: Task to delete.
        """
        await self.stop_backend(session_id, task_id)

        task_d = self.task_dir(session_id, task_id)
        if task_d.exists():
            shutil.rmtree(task_d)
            logger.info(f"[workspace] deleted {task_d}")

        self._registry.get(session_id, {}).pop(task_id, None)

    # ── global shutdown ───────────────────────────────────────────────────

    async def shutdown_all(self) -> None:
        """Stop all running backend subprocesses. Call on agent shutdown."""
        for session_id, tasks in list(self._registry.items()):
            for task_id in list(tasks.keys()):
                await self.stop_backend(session_id, task_id)
        logger.info("[workspace] all backends stopped")

    # ── private ───────────────────────────────────────────────────────────

    async def _install_requirements(self, task_dir: Path) -> None:
        req = task_dir / "requirements.txt"
        if not req.exists():
            return
        logger.info(f"[workspace] pip install for {task_dir.name}")
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "pip", "install", "-r", str(req), "--quiet",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            logger.warning(
                f"[workspace] pip install failed: {stderr.decode()[:400]}"
            )
