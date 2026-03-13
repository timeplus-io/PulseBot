"""Base classes for the tool call hook system."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Literal

from pydantic import BaseModel, model_validator


class HookVerdict(BaseModel):
    """Result from a pre-call hook."""

    verdict: Literal["approve", "deny", "modify"]
    modified_arguments: dict[str, Any] | None = None
    reasoning: str | None = None

    @model_validator(mode="after")
    def check_modify_has_arguments(self) -> "HookVerdict":
        """Ensure 'modify' verdict always carries modified_arguments."""
        if self.verdict == "modify" and self.modified_arguments is None:
            raise ValueError(
                "'modified_arguments' must be provided when verdict is 'modify'"
            )
        return self


class ToolCallHook(ABC):
    """Abstract base for pre/post tool call hooks.

    Implement ``pre_call`` to intercept tool calls before execution.
    Implement ``post_call`` for observability after execution.
    """

    async def setup(self) -> None:
        """Optional lifecycle: called once when the hook is initialized."""

    async def teardown(self) -> None:
        """Optional lifecycle: called once when the agent shuts down."""

    @abstractmethod
    async def pre_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> HookVerdict:
        """Inspect/approve/deny/modify a tool call before execution."""

    @abstractmethod
    async def post_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
        session_id: str = "",
    ) -> None:
        """Observe a tool call result after execution (no return value)."""
