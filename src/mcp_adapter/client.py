# Client for interacting with the RAG API Server

import requests # Assuming use of requests library, add to requirements.txt later if needed
import os

# Default URL for the RAG API server, can be overridden by environment variable
RAG_API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000") # Default to localhost:8000

def query_rag_api(query: str) -> dict:
    """
    Sends a query to the RAG API server and returns the response.

    Args:
        query: The natural language query string.

    Returns:
        A dictionary containing the answer and sources, or raises an exception on error.
    """
    endpoint = f"{RAG_API_URL}/query"
    payload = {"query": query}
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying RAG API: {e}")
        # Re-raise or handle appropriately
        raise

# Example usage (for testing purposes)
if __name__ == "__main__":
    test_query = "What is RAG?"
    try:
        result = query_rag_api(test_query)
        print("API Response:")
        print(result)
    except Exception as e:
        print(f"Failed to query API: {e}")
