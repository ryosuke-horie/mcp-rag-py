"""MCPアダプターのメインモジュール"""

import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .client import RAGApiClient
from .config import settings

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)

if settings.log_file:
    log_file_path = Path(settings.log_file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(settings.log_file)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)

# FastAPIアプリケーションの作成
app = FastAPI(
    title="RAG MCP Adapter",
    description="RAG APIサーバーとMCPの間のアダプター",
    version="0.1.0",
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG APIクライアントの初期化
rag_client = RAGApiClient(settings.rag_api_base_url)


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    try:
        # RAG APIサーバーのヘルスチェック
        rag_health = await rag_client.health_check()
        return {
            "status": "healthy",
            "rag_api": rag_health,
        }
    except Exception as e:
        logger.error(f"ヘルスチェックエラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search(query: str):
    """検索エンドポイント"""
    try:
        # RAG APIサーバーで検索を実行
        results = await rag_client.search(query)
        return results
    except Exception as e:
        logger.error(f"検索エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_content")
async def add_content(content: str):
    """コンテンツ追加エンドポイント"""
    try:
        # RAG APIサーバーにコンテンツを追加
        result = await rag_client.add_content(content)
        return result
    except Exception as e:
        logger.error(f"コンテンツ追加エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
