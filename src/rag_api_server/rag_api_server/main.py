from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

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
    print("RAGCoreの初期化が完了しました。")

    yield

    # アプリケーション終了時の処理
    if rag_core:
        rag_core.close()
        print("RAGCoreのリソースを解放しました。")


app = FastAPI(
    title="RAG API Server",
    description="RAGシステムの機能を提供するAPIサーバー",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "リクエストの検証に失敗しました", "errors": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# リクエスト/レスポンスモデル
class DocumentRequest(BaseModel):
    source_path: str = Field(
        ..., description="処理対象のドキュメントが格納されているディレクトリパス"
    )
    glob_pattern: str = Field(
        default="**/*[.md|.txt]", description="処理対象ファイルのフィルタリングパターン"
    )


class ContentRequest(BaseModel):
    content: str = Field(..., description="処理対象のテキストコンテンツ")
    metadata: dict[str, Any] | None = Field(
        default=None, description="コンテンツに関連するメタデータ"
    )


class QueryRequest(BaseModel):
    query: str = Field(..., description="検索クエリのテキスト")
    k: int = Field(default=4, description="返却する類似ドキュメントの数")
    filter_criteria: dict[str, Any] | None = Field(
        default=None, description="検索結果をフィルタリングするための条件"
    )


# APIエンドポイント
@app.post("/process-directory")
async def process_directory(request: DocumentRequest) -> dict[str, Any]:
    """
    指定されたディレクトリ内のドキュメントを処理し、ベクトルDBに保存する
    """
    if not rag_core:
        raise HTTPException(status_code=500, detail="RAGCoreが初期化されていません")
    return await rag_core.process_directory(
        request.source_path, glob_pattern=request.glob_pattern
    )


@app.post("/add-content")
async def add_content(request: ContentRequest) -> dict[str, Any]:
    """
    単一のテキストコンテンツを処理し、ベクトルDBに保存する
    """
    if not rag_core:
        raise HTTPException(status_code=500, detail="RAGCoreが初期化されていません")
    return await rag_core.add_single_content(request.content, metadata=request.metadata)


@app.post("/query")
async def query(request: QueryRequest) -> dict[str, Any]:
    """
    クエリに対して類似ドキュメントを検索する
    """
    if not rag_core:
        raise HTTPException(status_code=500, detail="RAGCoreが初期化されていません")
    return await rag_core.query(
        request.query, k=request.k, filter_criteria=request.filter_criteria
    )


# 基本的なルート
@app.get("/")
async def root():
    """
    APIサーバーの状態を確認するためのヘルスチェックエンドポイント
    """
    return {"status": "healthy", "version": app.version}
