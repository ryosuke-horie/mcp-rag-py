"""RAGシステム用のMCPサーバー実装"""

import logging
import os
import sys

# モジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from mcp.server.fastmcp import Context, FastMCP

from mcp_adapter.client import rag_client
from mcp_adapter.config import settings

# ロギングの設定
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp_adapter")

# MCPサーバーの作成
mcp = FastMCP(settings.server_name)


@mcp.tool()
async def search_documents(query: str, top_k: int = 5, ctx: Context = None) -> str:
    """クエリに基づいて関連ドキュメントを検索する

    Args:
        query: 検索クエリ
        top_k: 返却する上位結果の数（デフォルト: 5）
        ctx: MCPコンテキスト（自動注入）

    Returns:
        検索結果を含むフォーマット済み文字列
    """
    if ctx:
        ctx.info(f"検索中: {query}")

    try:
        response_data = await rag_client.search(query, top_k)
        results = response_data.get("results", [])

        if not results:
            return "関連するドキュメントが見つかりませんでした。"

        formatted_results = "## 検索結果\n\n"
        for i, result in enumerate(results, 1):
            text = result.get("text", "コンテンツが利用できません")
            similarity = result.get("similarity", 0.0)
            formatted_results += (
                f"### 結果 {i} (類似度: {similarity:.4f})\n\n{text}\n\n"
            )

        return formatted_results

    except Exception as e:
        logger.error(f"ドキュメント検索エラー: {e}")
        return f"ドキュメント検索エラー: {str(e)}"


@mcp.tool()
async def add_content(
    content: str,
    source_description: str | None = None,
    source_url: str | None = None,
    ctx: Context = None,
) -> str:
    """RAGシステムにテキストコンテンツを追加する。コンテンツはチャンク化され、埋め込みが生成される。

    Args:
        content: 追加するテキストコンテンツ
        source_description: コンテンツのソースの説明（オプション）
        source_url: コンテンツのソースURL（オプション）
        ctx: MCPコンテキスト（自動注入）

    Returns:
        コンテンツ追加に関するステータスメッセージ
    """
    if ctx:
        ctx.info(f"コンテンツ追加中 (ソース: {source_description or '不明'})")

    try:
        metadata = {}
        if source_description:
            metadata["source_description"] = source_description
        if source_url:
            metadata["source_url"] = source_url

        result = await rag_client.add_content(content, metadata if metadata else None)

        if result.get("status") == "success":
            processed_chunks = result.get("processed_chunks", "N/A")
            return f"コンテンツが正常に追加されました。{processed_chunks}個のチャンクを処理しました。"
        else:
            error_message = result.get("message", "不明なエラー")
            return f"コンテンツの追加に失敗しました: {error_message}"

    except Exception as e:
        logger.error(f"コンテンツ追加エラー: {e}")
        return f"コンテンツ追加エラー: {str(e)}"


@mcp.tool()
async def check_rag_status(ctx: Context = None) -> str:
    """RAG APIサーバーの状態を確認する

    Args:
        ctx: MCPコンテキスト（自動注入）

    Returns:
        RAG APIサーバーの状態情報
    """
    if ctx:
        ctx.info("RAG APIサーバーの状態を確認中")

    try:
        status = await rag_client.health_check()
        return f"RAG APIサーバーは動作中です: {status}"

    except Exception as e:
        logger.error(f"RAG APIサーバーの状態確認エラー: {e}")
        return f"RAG APIサーバーは利用できないようです: {str(e)}"


@mcp.resource("rag-info://status")
async def get_rag_status() -> str:
    """RAGシステムの現在の状態を取得する

    Returns:
        RAGシステムの状態情報を含むフォーマット済み文字列
    """
    try:
        status = await rag_client.health_check()
        return f"# RAGシステムの状態\n\n- 状態: オンライン\n- バージョン: {status.get('version', '不明')}\n- APIエンドポイント: {settings.rag_api_base_url}"

    except Exception as e:
        logger.error(f"RAGシステムの状態取得エラー: {e}")
        return "# RAGシステムの状態\n\n- 状態: オフライン\n- エラー: RAG APIサーバーに接続できません"
