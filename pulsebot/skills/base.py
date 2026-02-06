"""Base skill interface for PulseBot."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ToolDefinition(BaseModel):
    """Definition of a tool provided by a skill.
    
    Uses OpenAI-compatible format for LLM tool calling.
    """
    
    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema
    
    def to_openai_format(self) -> dict[str, Any]:
        """Convert to OpenAI tool format.
        
        Returns:
            Tool definition in OpenAI format
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ToolResult(BaseModel):
    """Result from tool execution."""
    
    success: bool
    output: Any
    error: str | None = None
    
    @classmethod
    def ok(cls, output: Any) -> "ToolResult":
        """Create a successful result.
        
        Args:
            output: The result output
            
        Returns:
            ToolResult with success=True
        """
        return cls(success=True, output=output)
    
    @classmethod
    def fail(cls, error: str) -> "ToolResult":
        """Create a failed result.
        
        Args:
            error: Error message
            
        Returns:
            ToolResult with success=False
        """
        return cls(success=False, output=None, error=error)


class BaseSkill(ABC):
    """Base class for all skills (tools).
    
    Skills provide tools that the agent can use to interact
    with external systems and perform actions.
    
    Example:
        >>> class MySkill(BaseSkill):
        ...     name = "my_skill"
        ...     description = "Does something useful"
        ...     
        ...     def get_tools(self) -> list[ToolDefinition]:
        ...         return [ToolDefinition(
        ...             name="do_thing",
        ...             description="Does the thing",
        ...             parameters={"type": "object", "properties": {}}
        ...         )]
        ...     
        ...     async def execute(self, tool_name: str, arguments: dict) -> ToolResult:
        ...         if tool_name == "do_thing":
        ...             return ToolResult.ok("Done!")
        ...         return ToolResult.fail(f"Unknown tool: {tool_name}")
    """
    
    name: str = "base_skill"
    description: str = "Base skill"
    
    @abstractmethod
    def get_tools(self) -> list[ToolDefinition]:
        """Return list of tools provided by this skill.
        
        Returns:
            List of tool definitions
        """
        pass
    
    @abstractmethod
    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        """Execute a tool with given arguments.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            ToolResult with success status and output
        """
        pass
    
    def get_tool_by_name(self, name: str) -> ToolDefinition | None:
        """Get a specific tool definition by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool definition or None if not found
        """
        for tool in self.get_tools():
            if tool.name == name:
                return tool
        return None
    
    def provides_tool(self, name: str) -> bool:
        """Check if this skill provides a specific tool.
        
        Args:
            name: Tool name to check
            
        Returns:
            True if skill provides the tool
        """
        return self.get_tool_by_name(name) is not None
