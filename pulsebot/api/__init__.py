"""FastAPI web server for PulseBot."""

from pulsebot.api.server import create_app, router

__all__ = [
    "create_app",
    "router",
]
