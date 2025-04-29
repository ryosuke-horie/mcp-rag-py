# Main entry point for the MCP Adapter Server using Python MCP SDK

import asyncio
import json
from modelcontextprotocol.server.mcp import McpServer
from modelcontextprotocol.server.stdio import StdioServerTransport
from modelcontextprotocol.server.tools import ToolResult
from modelcontextprotocol.server.exceptions import McpError

# Import the tool definition and its input schema
from .mcp_spec import query_rag_tool, QueryRagInput
# Import the client function to call the RAG API
from .client import query_rag_api

async def handle_query_rag_system(params: QueryRagInput) -> ToolResult:
    """
    Async handler function for the 'query_rag_system' tool.
    Calls the RAG API client and returns the result.
    """
    print(f"Executing query_rag_system with query: '{params.query}', top_k: {params.top_k}")
    try:
        # Call the client function that interacts with rag_api_server
        # Note: query_rag_api currently only takes 'query'.
        # If top_k needs to be passed, client.py needs modification.
        # For now, we only pass the query.
        api_response = query_rag_api(query=params.query)

        # Format the response as a JSON string for ToolResult content
        # Assuming api_response is a dictionary like {'results': [...]}
        content_json = json.dumps(api_response, ensure_ascii=False, indent=2)

        print(f"API Response received, returning ToolResult.")
        return ToolResult(content=content_json)

    except Exception as e:
        error_message = f"Error executing query_rag_system: {e}"
        print(error_message)
        # Convert the exception to an McpError for the client
        raise McpError(message=error_message)

# Assign the actual handler function to the tool instance
query_rag_tool.handler = handle_query_rag_system

# --- MCP Server Setup ---

# Create the McpServer instance
server = McpServer(
    name="rag-mcp-adapter", # Choose a suitable name
    version="0.1.0"
)

# Add the defined tool(s) to the server instance
server.add_tool(query_rag_tool)
# server.add_root(...) # Add roots if resources are defined

# --- Server Execution ---

async def main():
    """
    Main async function to run the MCP server with StdioTransport.
    """
    # Use StdioServerTransport for communication via standard input/output
    transport = StdioServerTransport(server)
    print("Starting MCP Adapter Server on stdio...")
    try:
        await transport.run()
    except Exception as e:
        print(f"MCP Server encountered an error: {e}")
    finally:
        print("MCP Adapter Server stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMCP Adapter Server interrupted by user.")
