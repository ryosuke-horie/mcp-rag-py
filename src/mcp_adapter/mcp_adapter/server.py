"""MCP server implementation for the RAG system."""

import logging
import os
import sys

# モジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
        # rag_client.search は {"results": [...]} を返す想定
        response_data = await rag_client.search(query, top_k)
        results = response_data.get("results", [])  # resultsキーからリストを取得

        if not results:
            return "No relevant documents found."

        formatted_results = "## Search Results\n\n"
        # results は [{'text': '...', 'similarity': 0.9}, ...] の形式
        for i, result in enumerate(results, 1):
            text = result.get("text", "No content available")
            similarity = result.get("similarity", 0.0)
            formatted_results += (
                f"### Result {i} (Similarity: {similarity:.4f})\n\n{text}\n\n"
            )

        return formatted_results

    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return f"Error searching documents: {str(e)}"


@mcp.tool()
async def add_content(
    content: str,
    source_description: str | None = None,
    source_url: str | None = None,
    ctx: Context = None,
) -> str:
    """Add text content to the RAG system. The content will be chunked and embedded.

    Args:
        content: The text content to add.
        source_description: Optional description of the content's source (e.g., "Brave Search result").
        source_url: Optional URL of the content's source.
        ctx: MCP context (auto-injected).

    Returns:
        Status message about the content addition.
    """
    if ctx:
        ctx.info(f"Adding content (Source: {source_description or 'Unknown'})")

    try:
        # メタデータを作成 (APIが受け取る形式に合わせる)
        metadata = {}
        if source_description:
            metadata["source_description"] = source_description
        if source_url:
            metadata["source_url"] = source_url

        # rag_client.add_content を呼び出す (metadataが空辞書でもOK)
        result = await rag_client.add_content(content, metadata if metadata else None)

        # APIからのレスポンスに基づいてメッセージを生成
        if result.get("status") == "success":
            processed_chunks = result.get("processed_chunks", "N/A")
            return f"Content added successfully. Processed {processed_chunks} chunks."
        else:
            error_message = result.get("message", "Unknown error")
            return f"Failed to add content: {error_message}"

    except Exception as e:
        logger.error(f"Error adding content: {e}")
        return f"Error adding content: {str(e)}"


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
