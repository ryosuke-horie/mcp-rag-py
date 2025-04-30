"""RAG APIサーバーのクライアントモジュール"""

import os
import sys

# モジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any

import httpx

from mcp_adapter.config import settings


class RAGApiClient:
    """RAG APIサーバーのクライアント"""

    def __init__(self, base_url: str | None = None):
        """RAG APIクライアントを初期化する

        Args:
            base_url: RAG APIサーバーのベースURL。指定しない場合は設定値を使用
        """
        self.base_url = base_url or settings.rag_api_base_url

    async def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """クエリに一致するドキュメントを検索する

        Args:
            query: 検索クエリ
            top_k: 返却する結果の数

        Returns:
            メタデータと類似度スコアを含む一致ドキュメントのリスト
        """
        url = f"{self.base_url}/search/"
        data = {"query": query, "top_k": top_k}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def add_content(
        self, content: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """RAGシステムにテキストコンテンツを追加する

        Args:
            content: 追加するテキストコンテンツ
            metadata: コンテンツに関連するメタデータ（オプション）

        Returns:
            RAG APIサーバーからのレスポンス（ステータス、メッセージ、処理されたチャンク数など）
        """
        url = f"{self.base_url}/contents/"
        data = {"content": content}
        if metadata:
            data["metadata"] = metadata

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def health_check(self) -> dict[str, Any]:
        """RAG APIサーバーの状態を確認する

        Returns:
            ヘルスステータス情報
        """
        url = f"{self.base_url}/"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()


# デフォルトのクライアントインスタンスを作成
rag_client = RAGApiClient()
