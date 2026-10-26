"""Vercel entry point. The application lives in server/."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.app import create_app  # noqa: E402

# ASGI app served by Vercel; the MCP endpoint is /mcp
app = create_app()
