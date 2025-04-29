# MCP Server Specification
# Defines the tools and resources provided by this MCP server.

# Example Tool Definition (to be refined)
TOOLS = [
    {
        "name": "query_rag_system",
        "description": "Query the RAG system with a natural language question and get an answer based on the indexed documents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The natural language query."
                }
            },
            "required": ["query"]
        }
        # output_schema can be defined later
    }
    # Potentially add a tool for indexing new documents later
]

RESOURCES = [] # No resources defined initially

def get_tools():
    """Returns the list of tools."""
    return TOOLS

def get_resources():
    """Returns the list of resources."""
    return RESOURCES
