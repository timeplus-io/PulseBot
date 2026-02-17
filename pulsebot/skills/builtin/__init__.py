"""Built-in skills for PulseBot."""

from pulsebot.skills.builtin.agentskills_bridge import AgentSkillsBridge
from pulsebot.skills.builtin.file_ops import FileOpsSkill
from pulsebot.skills.builtin.shell import ShellSkill
from pulsebot.skills.builtin.web_search import WebSearchSkill

__all__ = [
    "AgentSkillsBridge",
    "WebSearchSkill",
    "FileOpsSkill",
    "ShellSkill",
]
