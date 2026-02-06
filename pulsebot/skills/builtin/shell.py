"""Shell command execution skill."""

from __future__ import annotations

import asyncio
import shlex
from typing import Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class ShellSkill(BaseSkill):
    """Shell command execution skill.
    
    Provides ability to run shell commands with safety guardrails.
    
    Example:
        >>> skill = ShellSkill(allowed_commands=["ls", "cat", "grep"])
        >>> result = await skill.execute("run_command", {"command": "ls -la"})
    """
    
    name = "shell"
    description = "Execute shell commands"
    
    # Commands that are blocked by default
    BLOCKED_COMMANDS = {
        "rm", "rmdir", "mv", "dd", "mkfs", "fdisk",
        "shutdown", "reboot", "halt", "init",
        "sudo", "su", "chmod", "chown",
        "format", "del", "erase",
    }
    
    def __init__(
        self,
        allowed_commands: list[str] | None = None,
        working_directory: str | None = None,
        timeout_seconds: int = 30,
        max_output_length: int = 10000,
    ):
        """Initialize shell skill.
        
        Args:
            allowed_commands: Whitelist of allowed commands (None = use blocklist)
            working_directory: Working directory for commands
            timeout_seconds: Command timeout
            max_output_length: Max output characters to return
        """
        self.allowed_commands = allowed_commands
        self.working_directory = working_directory
        self.timeout_seconds = timeout_seconds
        self.max_output_length = max_output_length
    
    def get_tools(self) -> list[ToolDefinition]:
        """Return shell tool definition."""
        return [
            ToolDefinition(
                name="run_command",
                description="Run a shell command and return its output. Use for tasks like listing files, checking system info, or running scripts.",
                parameters={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute"
                        }
                    },
                    "required": ["command"]
                }
            ),
        ]
    
    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        """Execute a shell command.
        
        Args:
            tool_name: Should be "run_command"
            arguments: Command arguments
            
        Returns:
            Command output
        """
        if tool_name != "run_command":
            return ToolResult.fail(f"Unknown tool: {tool_name}")
        
        command = arguments.get("command", "")
        if not command:
            return ToolResult.fail("Command is required")
        
        # Validate command
        validation_error = self._validate_command(command)
        if validation_error:
            return ToolResult.fail(validation_error)
        
        try:
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.working_directory,
            )
            
            # Wait with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout_seconds,
                )
            except asyncio.TimeoutError:
                process.kill()
                return ToolResult.fail(f"Command timed out after {self.timeout_seconds}s")
            
            # Decode output
            stdout_str = stdout.decode("utf-8", errors="replace")
            stderr_str = stderr.decode("utf-8", errors="replace")
            
            # Truncate if needed
            if len(stdout_str) > self.max_output_length:
                stdout_str = stdout_str[:self.max_output_length] + "\n... (output truncated)"
            if len(stderr_str) > self.max_output_length:
                stderr_str = stderr_str[:self.max_output_length] + "\n... (output truncated)"
            
            result = {
                "exit_code": process.returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
            }
            
            if process.returncode != 0:
                logger.warning(
                    "Command returned non-zero exit code",
                    extra={"command": command[:50], "exit_code": process.returncode}
                )
            
            return ToolResult.ok(result)
            
        except Exception as e:
            return ToolResult.fail(f"Command execution failed: {e}")
    
    def _validate_command(self, command: str) -> str | None:
        """Validate a command against security rules.
        
        Args:
            command: Command to validate
            
        Returns:
            Error message if invalid, None if valid
        """
        try:
            # Parse command to get the base command
            parts = shlex.split(command)
            if not parts:
                return "Empty command"
            
            base_command = parts[0].split("/")[-1]  # Get basename
            
            # Check whitelist mode
            if self.allowed_commands is not None:
                if base_command not in self.allowed_commands:
                    return f"Command '{base_command}' is not in the allowed list"
            else:
                # Check blocklist mode
                if base_command.lower() in self.BLOCKED_COMMANDS:
                    return f"Command '{base_command}' is blocked for safety"
            
            # Check for dangerous patterns
            dangerous_patterns = [
                "| rm", "| sudo", "; rm", "; sudo",
                "&& rm", "&& sudo", "$(rm", "$(sudo",
                "`rm", "`sudo", "> /dev/", "| dd",
            ]
            
            command_lower = command.lower()
            for pattern in dangerous_patterns:
                if pattern in command_lower:
                    return f"Command contains dangerous pattern: {pattern}"
            
            return None
            
        except ValueError as e:
            return f"Invalid command syntax: {e}"
