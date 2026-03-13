"""Tool executor for running skill tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.hooks.base import ToolCallHook

logger = get_logger(__name__)


class ToolExecutor:
    """Execute tools from loaded skills.

    Dispatches tool calls to the appropriate skill handlers and
    logs execution results back to the messages stream.

    Example:
        >>> executor = ToolExecutor(skill_loader)
        >>> result = await executor.execute("shell", {"command": "ls -l"})
    """

    def __init__(self, skill_loader: "SkillLoader", hooks: "list[ToolCallHook] | None" = None):
        """Initialize tool executor.

        Args:
            skill_loader: Loaded skills manager
            hooks: Optional list of ToolCallHook instances for pre/post execution
        """
        self.skills = skill_loader
        self._hooks: list[ToolCallHook] = hooks if hooks is not None else []
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
            if not tool_name:
                inferred_name = self._infer_tool_from_args(arguments)
                if inferred_name:
                    logger.warning(
                        "Inferred empty tool name from arguments",
                        extra={"inferred_tool": inferred_name, "arguments": arguments}
                    )
                    tool_name = inferred_name
                else:
                    return {
                        "success": False,
                        "output": None,
                        "error": "Invalid tool call: tool name is empty and could not be inferred.",
                    }

            # Run pre-call hooks; allow modification or denial of the call
            effective_arguments = dict(arguments)
            for hook in self._hooks:
                verdict = await hook.pre_call(tool_name, effective_arguments, session_id)
                if verdict.verdict == "deny":
                    reason = verdict.reasoning or "no reason given"
                    logger.warning(
                        "Tool call denied by hook",
                        extra={"tool": tool_name, "hook": type(hook).__name__, "reason": reason},
                    )
                    return {
                        "success": False,
                        "output": None,
                        "error": f"Tool call denied by {type(hook).__name__}: {reason}",
                    }
                if verdict.verdict == "modify" and verdict.modified_arguments is not None:
                    effective_arguments = verdict.modified_arguments

            # Find the skill that provides this tool
            skill = self.skills.get_skill_for_tool(tool_name)

            if skill is None:
                return {
                    "success": False,
                    "output": None,
                    "error": f"Unknown tool: {tool_name}",
                }

            # Execute the tool with (potentially modified) arguments
            result = await skill.execute(tool_name, effective_arguments)

            logger.info(
                "Tool execution complete",
                extra={
                    "tool": tool_name,
                    "success": result.success,
                    "execution_id": self._execution_count,
                }
            )

            result_dict = {
                "success": result.success,
                "output": result.output,
                "error": result.error,
            }

            # Run post-call hooks; errors are logged but do not affect the result
            for hook in self._hooks:
                try:
                    await hook.post_call(tool_name, effective_arguments, result_dict, session_id)
                except Exception as post_exc:
                    logger.warning(
                        "Post-call hook raised an exception",
                        extra={"hook": type(hook).__name__, "error": str(post_exc)},
                    )

            return result_dict

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
    
    def _infer_tool_from_args(self, arguments: dict[str, Any]) -> str | None:
        """Attempt to infer the missing tool name based on provided argument keys.
        
        Matches argument keys against tool schemas. Returns tool name if exactly one matches.
        """
        if not arguments:
            return None
            
        arg_keys = set(arguments.keys())
        definitions = self.get_tool_definitions()
        
        possible_tools = []
        for d in definitions:
            if d.get("type") == "function":
                func = d.get("function", {})
                name = func.get("name")
                params = func.get("parameters", {})
                
                required_keys = set(params.get("required", []))
                allowed_keys = set(params.get("properties", {}).keys())
                
                # Check if this tool is a valid match
                # 1. All provided arguments must be known parameters for this tool
                # 2. All required parameters must be present in the provided arguments
                if arg_keys.issubset(allowed_keys) and required_keys.issubset(arg_keys):
                    possible_tools.append(name)
                    
        if len(possible_tools) == 1:
            return possible_tools[0]
            
        return None
    
    @property
    def execution_count(self) -> int:
        """Total number of tool executions."""
        return self._execution_count
