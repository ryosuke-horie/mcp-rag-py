"""MCP server implementation for the RAG system."""

import logging
import sys
import os

# モジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context, FastMCP

from mcp_adapter.client import rag_client
from mcp_adapter.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp_adapter")

# Create MCP server
mcp = FastMCP(settings.server_name)


@mcp.tool()
async def search_documents(query: str, top_k: int = 5, ctx: Context = None) -> str:
    """Search for relevant documents based on the query.
    
    Args:
        query: The search query.
        top_k: Number of top results to return (default: 5).
        ctx: MCP context (auto-injected).
    
    Returns:
        Formatted string with search results.
    """
    if ctx:
        ctx.info(f"Searching for: {query}")
    
    try:
        results = await rag_client.search(query, top_k)
        
        if not results:
            return "No relevant documents found."
        
        formatted_results = "## Search Results\n\n"
        for i, result in enumerate(results, 1):
            content = result.get("content", "No content available")
            score = result.get("score", 0.0)
            formatted_results += f"### Result {i} (Similarity: {score:.4f})\n\n{content}\n\n"
        
        return formatted_results
    
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return f"Error searching documents: {str(e)}"


@mcp.tool()
async def add_document(content: str, title: Optional[str] = None, ctx: Context = None) -> str:
    """Add a new document to the RAG system.
    
    Args:
        content: The document content.
        title: Optional document title.
        ctx: MCP context (auto-injected).
    
    Returns:
        Status message about the document addition.
    """
    if ctx:
        ctx.info(f"Adding document: {title if title else 'Untitled'}")
    
    try:
        metadata = {"title": title} if title else {}
        result = await rag_client.add_document(content, metadata)
        
        return f"Document added successfully with ID: {result.get('id')}."
    
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        return f"Error adding document: {str(e)}"


@mcp.tool()
async def check_rag_status(ctx: Context = None) -> str:
    """Check the status of the RAG API Server.
    
    Args:
        ctx: MCP context (auto-injected).
    
    Returns:
        Status information about the RAG API Server.
    """
    if ctx:
        ctx.info("Checking RAG API Server status")
    
    try:
        status = await rag_client.health_check()
        return f"RAG API Server is operational: {status}"
    
    except Exception as e:
        logger.error(f"Error checking RAG API Server status: {e}")
        return f"RAG API Server appears to be unavailable: {str(e)}"


@mcp.resource("rag-info://status")
async def get_rag_status() -> str:
    """Get the current status of the RAG system.
    
    Returns:
        Formatted string with RAG system status information.
    """
    try:
        status = await rag_client.health_check()
        return f"# RAG System Status\n\n- Status: Online\n- Version: {status.get('version', 'Unknown')}\n- API Endpoint: {settings.rag_api_base_url}"
    
    except Exception as e:
        logger.error(f"Error getting RAG system status: {e}")
        return "# RAG System Status\n\n- Status: Offline\n- Error: Unable to connect to RAG API Server"
