"""Main application module."""

import logging

import uvicorn

from .config import settings
from .server import mcp

logger = logging.getLogger("mcp_adapter")


def main():
    """Run the MCP server."""
    logger.info(f"Starting MCP server: {settings.server_name}")
    logger.info(f"RAG API Server: {settings.rag_api_base_url}")
    
    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
