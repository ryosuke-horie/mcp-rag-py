"""RAG API Server client module."""

import json
from typing import Any, Dict, List, Optional

import httpx

from .config import settings


class RAGApiClient:
    """Client for the RAG API Server."""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize the RAG API client.

        Args:
            base_url: Base URL of the RAG API Server. Defaults to the configured URL.
        """
        self.base_url = base_url or settings.rag_api_base_url

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for documents matching the query.

        Args:
            query: The search query.
            top_k: Number of results to return.

        Returns:
            List of matching documents with their metadata and similarity scores.
        """
        url = f"{self.base_url}/search/"
        data = {"query": query, "top_k": top_k}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a document to the RAG system.

        Args:
            content: The document content.
            metadata: Optional document metadata.

        Returns:
            The created document information.
        """
        url = f"{self.base_url}/documents/"
        data = {"content": content}
        if metadata:
            data["metadata"] = metadata
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def health_check(self) -> Dict[str, Any]:
        """Check if the RAG API Server is healthy.

        Returns:
            Health status information.
        """
        url = f"{self.base_url}/"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()


# Create a default client instance
rag_client = RAGApiClient()
