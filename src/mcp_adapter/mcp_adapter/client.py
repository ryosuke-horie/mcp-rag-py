"""RAG API Server client module."""

import json
import sys
import os

# モジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, List, Optional

import httpx

from mcp_adapter.config import settings


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
            # searchの結果は {"results": [...]} の形式なので、それをそのまま返す
            return response.json()

    async def add_content(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add text content to the RAG system via the /contents/ endpoint.

        Args:
            content: The text content to add.
            metadata: Optional metadata associated with the content.

        Returns:
            The response from the RAG API server (e.g., status, message, processed_chunks).
        """
        url = f"{self.base_url}/contents/" # 新しいエンドポイントに変更
        data = {"content": content}
        if metadata:
            data["metadata"] = metadata # metadataも送信

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status() # エラーがあれば例外発生
            return response.json() # APIからのレスポンスをそのまま返す

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
