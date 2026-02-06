"""Tool executor for running skill tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.skills.loader import SkillLoader

logger = get_logger(__name__)


class ToolExecutor:
    """Execute tools from loaded skills.
    
    Dispatches tool calls to the appropriate skill handlers and
    logs execution results back to the messages stream.
    
    Example:
        >>> executor = ToolExecutor(skill_loader)
        >>> result = await executor.execute("web_search", {"query": "weather"})
    """
    
    def __init__(self, skill_loader: "SkillLoader"):
        """Initialize tool executor.
        
        Args:
            skill_loader: Loaded skills manager
        """
        self.skills = skill_loader
        self._execution_count = 0
    
    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        session_id: str = "",
    ) -> dict[str, Any]:
        """Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            session_id: Current session ID for logging
            
        Returns:
            Tool result dict with 'success', 'output', and optionally 'error'
        """
        self._execution_count += 1
        
        logger.info(
            "Executing tool",
            extra={
                "tool": tool_name,
                "session_id": session_id,
                "execution_id": self._execution_count,
            }
        )
        
        try:
            # Find the skill that provides this tool
            skill = self.skills.get_skill_for_tool(tool_name)
            
            if skill is None:
                return {
                    "success": False,
                    "output": None,
                    "error": f"Unknown tool: {tool_name}",
                }
            
            # Execute the tool
            result = await skill.execute(tool_name, arguments)
            
            logger.info(
                "Tool execution complete",
                extra={
                    "tool": tool_name,
                    "success": result.success,
                    "execution_id": self._execution_count,
                }
            )
            
            return {
                "success": result.success,
                "output": result.output,
                "error": result.error,
            }
            
        except Exception as e:
            logger.error(
                "Tool execution failed",
                extra={
                    "tool": tool_name,
                    "error": str(e),
                    "execution_id": self._execution_count,
                }
            )
            
            return {
                "success": False,
                "output": None,
                "error": str(e),
            }
    
    async def execute_batch(
        self,
        tool_calls: list[dict[str, Any]],
        session_id: str = "",
    ) -> list[dict[str, Any]]:
        """Execute multiple tool calls.
        
        Executes tools sequentially to maintain ordering.
        
        Args:
            tool_calls: List of tool call dicts with 'name' and 'arguments'
            session_id: Current session ID
            
        Returns:
            List of result dicts
        """
        results = []
        for tc in tool_calls:
            result = await self.execute(
                tool_name=tc.get("name", ""),
                arguments=tc.get("arguments", {}),
                session_id=session_id,
            )
            results.append(result)
        return results
    
    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """Get all available tool definitions.
        
        Returns:
            List of tool definitions in OpenAI format
        """
        return self.skills.get_tool_definitions()
    
    @property
    def execution_count(self) -> int:
        """Total number of tool executions."""
        return self._execution_count
