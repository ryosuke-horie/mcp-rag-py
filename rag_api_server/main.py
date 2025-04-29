from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from .core import RAGCore

# グローバル変数としてRAGCoreインスタンスを保持
rag_core: RAGCore | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPIアプリケーションのライフサイクルを管理する
    """
    # アプリケーション起動時の処理
    global rag_core
    rag_core = RAGCore()
    print("RAGCore initialized.")
    
    yield
    
    # アプリケーション終了時の処理
    if rag_core:
        rag_core.close()
        print("RAGCore resources released.")

app = FastAPI(
    title="RAG API Server",
    description="RAGシステムの機能を提供するAPIサーバー",
    version="0.1.0",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエスト/レスポンスモデル
class DocumentRequest(BaseModel):
    source_path: str = Field(..., description="処理対象のドキュメントが格納されているディレクトリパス")
    glob_pattern: str = Field(default="**/*[.md|.txt]", description="処理対象ファイルのフィルタリングパターン")

class SearchRequest(BaseModel):
    query: str = Field(..., description="検索クエリ")
    top_k: int = Field(default=5, ge=1, le=100, description="返す結果の最大数")

class SearchResult(BaseModel):
    text: str = Field(..., description="検索結果のテキスト")
    similarity: float = Field(..., description="クエリとの類似度スコア")

class SearchResponse(BaseModel):
    results: List[SearchResult] = Field(..., description="検索結果のリスト")

# 基本的なルート
@app.get("/")
async def root():
    """
    APIサーバーの状態を確認するためのヘルスチェックエンドポイント
    """
    return {
        "status": "healthy",
        "version": app.version
    }

# ドキュメント処理エンドポイント
@app.post("/documents/")
async def create_documents(request: DocumentRequest) -> Dict[str, Any]:
    """
    指定されたパスのドキュメントを処理し、ベクトルDBに保存します。
    """
    if not rag_core:
        raise HTTPException(status_code=500, detail="RAGCore is not initialized")

    result = await rag_core.process_directory(
        directory_path=request.source_path,
        glob_pattern=request.glob_pattern
    )

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

# 検索エンドポイント
@app.post("/search/", response_model=SearchResponse)
async def search_documents(request: SearchRequest) -> SearchResponse:
    """
    指定されたクエリに基づいて関連ドキュメントを検索します。
    """
    if not rag_core:
        raise HTTPException(status_code=500, detail="RAGCore is not initialized")

    try:
        results = await rag_core.search(query=request.query, top_k=request.top_k)
        return SearchResponse(results=[
            SearchResult(text=result["text"], similarity=result["similarity"])
            for result in results
        ])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
