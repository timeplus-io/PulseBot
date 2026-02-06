"""File operations skill."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class FileOpsSkill(BaseSkill):
    """File operations skill for reading, writing, and listing files.
    
    Example:
        >>> skill = FileOpsSkill(base_path="/home/user")
        >>> result = await skill.execute("read_file", {"path": "notes.txt"})
    """
    
    name = "file_ops"
    description = "Read, write, and list files"
    
    def __init__(self, base_path: str = ".", allowed_extensions: list[str] | None = None):
        """Initialize file operations skill.
        
        Args:
            base_path: Base directory for file operations
            allowed_extensions: Allowed file extensions (None = all)
        """
        self.base_path = Path(base_path).resolve()
        self.allowed_extensions = allowed_extensions
    
    def get_tools(self) -> list[ToolDefinition]:
        """Return file operation tool definitions."""
        return [
            ToolDefinition(
                name="read_file",
                description="Read the contents of a file",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file (relative to base path)"
                        }
                    },
                    "required": ["path"]
                }
            ),
            ToolDefinition(
                name="write_file",
                description="Write content to a file (creates if not exists)",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file (relative to base path)"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write"
                        },
                        "append": {
                            "type": "boolean",
                            "description": "Append to file instead of overwriting",
                            "default": False
                        }
                    },
                    "required": ["path", "content"]
                }
            ),
            ToolDefinition(
                name="list_directory",
                description="List files and directories in a path",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path (relative to base path)",
                            "default": "."
                        }
                    }
                }
            ),
        ]
    
    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        """Execute a file operation.
        
        Args:
            tool_name: Tool to execute
            arguments: Tool arguments
            
        Returns:
            Operation result
        """
        if tool_name == "read_file":
            return await self._read_file(arguments)
        elif tool_name == "write_file":
            return await self._write_file(arguments)
        elif tool_name == "list_directory":
            return await self._list_directory(arguments)
        else:
            return ToolResult.fail(f"Unknown tool: {tool_name}")
    
    def _resolve_path(self, path: str) -> Path | None:
        """Resolve and validate a path.
        
        Args:
            path: Relative path
            
        Returns:
            Resolved path or None if invalid
        """
        try:
            resolved = (self.base_path / path).resolve()
            
            # Security: ensure path is within base_path
            if not str(resolved).startswith(str(self.base_path)):
                return None
            
            return resolved
        except Exception:
            return None
    
    def _check_extension(self, path: Path) -> bool:
        """Check if file extension is allowed.
        
        Args:
            path: File path
            
        Returns:
            True if allowed
        """
        if self.allowed_extensions is None:
            return True
        return path.suffix.lstrip(".") in self.allowed_extensions
    
    async def _read_file(self, arguments: dict[str, Any]) -> ToolResult:
        """Read file contents."""
        path_str = arguments.get("path", "")
        path = self._resolve_path(path_str)
        
        if path is None:
            return ToolResult.fail("Invalid or disallowed path")
        
        if not path.exists():
            return ToolResult.fail(f"File not found: {path_str}")
        
        if not path.is_file():
            return ToolResult.fail(f"Not a file: {path_str}")
        
        if not self._check_extension(path):
            return ToolResult.fail(f"File extension not allowed: {path.suffix}")
        
        try:
            content = path.read_text()
            return ToolResult.ok({"path": path_str, "content": content})
        except Exception as e:
            return ToolResult.fail(f"Failed to read file: {e}")
    
    async def _write_file(self, arguments: dict[str, Any]) -> ToolResult:
        """Write file contents."""
        path_str = arguments.get("path", "")
        content = arguments.get("content", "")
        append = arguments.get("append", False)
        
        path = self._resolve_path(path_str)
        
        if path is None:
            return ToolResult.fail("Invalid or disallowed path")
        
        if not self._check_extension(path):
            return ToolResult.fail(f"File extension not allowed: {path.suffix}")
        
        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            mode = "a" if append else "w"
            with open(path, mode) as f:
                f.write(content)
            
            return ToolResult.ok({"path": path_str, "bytes_written": len(content)})
        except Exception as e:
            return ToolResult.fail(f"Failed to write file: {e}")
    
    async def _list_directory(self, arguments: dict[str, Any]) -> ToolResult:
        """List directory contents."""
        path_str = arguments.get("path", ".")
        path = self._resolve_path(path_str)
        
        if path is None:
            return ToolResult.fail("Invalid or disallowed path")
        
        if not path.exists():
            return ToolResult.fail(f"Directory not found: {path_str}")
        
        if not path.is_dir():
            return ToolResult.fail(f"Not a directory: {path_str}")
        
        try:
            items = []
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                })
            
            return ToolResult.ok({"path": path_str, "items": items})
        except Exception as e:
            return ToolResult.fail(f"Failed to list directory: {e}")
