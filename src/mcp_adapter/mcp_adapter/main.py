"""Main application module."""

import logging
import sys
import os

# モジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn

from mcp_adapter.config import settings
from mcp_adapter.server import mcp

logger = logging.getLogger("mcp_adapter")


def main():
    """Run the MCP server."""
    logger.info(f"Starting MCP server: {settings.server_name}")
    logger.info(f"RAG API Server: {settings.rag_api_base_url}")
    
    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
