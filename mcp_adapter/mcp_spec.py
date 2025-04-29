# MCP Server Specification using Python MCP SDK
# Defines the tools provided by this MCP server.

from pydantic import BaseModel, Field
from modelcontextprotocol.server.tools import Tool
from typing import Awaitable, Callable, Any

# Define the input schema for the query tool using Pydantic
class QueryRagInput(BaseModel):
    query: str = Field(..., description="The natural language query.")
    top_k: int = Field(default=5, ge=1, le=100, description="The maximum number of results to return.")

# Placeholder for the actual handler function which will be defined in main.py
# The handler must be an async function that accepts the Pydantic model instance
# and returns a ToolResult.
async def placeholder_handler(params: QueryRagInput) -> Any:
    raise NotImplementedError("Handler not implemented yet.")

# Define the tool using the Tool class from the SDK
query_rag_tool = Tool(
    name="query_rag_system",
    description="Query the RAG system with a natural language question and get relevant document snippets.",
    input_schema=QueryRagInput.model_json_schema(),
    # The actual handler function will be assigned in main.py when setting up the server
    handler=placeholder_handler, # Assign the actual async handler function here
)

# List of tools to be registered with the McpServer instance
TOOLS = [
    query_rag_tool,
    # Potentially add a tool for indexing new documents later
]

# Resources are not defined for now
RESOURCES = []

# Functions to easily retrieve tools/resources if needed elsewhere,
# although direct registration to McpServer is common.
def get_tools() -> list[Tool]:
    """Returns the list of defined tools."""
    return TOOLS

def get_resources() -> list:
    """Returns the list of defined resources."""
    return RESOURCES
