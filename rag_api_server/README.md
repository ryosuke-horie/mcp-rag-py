# RAG API Server

このディレクトリには、RAG (Retrieval-Augmented Generation) コア機能への API アクセスを提供する FastAPI サーバーの実装が含まれます。

## 目的

`rag_core` コンポーネント（ドキュメント処理、埋め込み生成、ベクトル検索）の機能を HTTP API として公開し、他のアプリケーション（例: MCP サーバー）から利用可能にすることを目的とします。

## 前提条件

- Python 3.10+
- DuckDB
- Ollama（`bge-m3`モデルがインストールされていること）

## 環境構築

1. プロジェクトのルートディレクトリ (`mcp-rag`) にいることを確認します。

2. 依存関係のインストール:
    ```bash
    pip install -r requirements.txt
    ```

3. Ollamaサーバーの起動と`bge-m3`モデルの準備:
    ```bash
    # Ollamaサーバーを起動（別ターミナルで）
    ollama serve

    # bge-m3モデルのプル
    ollama pull bge-m3
    ```

## 設定

以下の環境変数で設定をカスタマイズできます：

- `RAG_OLLAMA_BASE_URL`: OllamaサーバーのベースURL（デフォルト: "http://localhost:11434"）
- `RAG_EMBEDDING_MODEL_NAME`: 使用する埋め込みモデル名（デフォルト: "bge-m3"）
- `RAG_DB_PATH`: DuckDBデータベースのパス（デフォルト: "vector_store.db"）
- `RAG_TABLE_NAME`: ベクトルを保存するテーブル名（デフォルト: "embeddings"）
- `RAG_CHUNK_SIZE`: テキスト分割時のチャンクサイズ（デフォルト: 1000）
- `RAG_CHUNK_OVERLAP`: チャンク間のオーバーラップサイズ（デフォルト: 200）

## サーバーの起動

1. プロジェクトのルートディレクトリ (`mcp-rag`) にいることを確認します。

2. 仮想環境を有効にします:
    ```bash
    # fish シェルの場合
    source .venv/bin/activate.fish 
    # bash/zsh の場合
    # source .venv/bin/activate
    ```

3. 以下のコマンドを実行します:
    ```bash 
    uvicorn rag_api_server.main:app --reload
    ```

サーバーが起動したら、http://localhost:8000/docs でSwagger UIにアクセスできます。

## API エンドポイント

### ヘルスチェック

```http
GET /
```

サーバーの状態を確認します。レスポンス例:
```json
{
    "status": "healthy",
    "version": "0.1.0"
}
```

### ドキュメントの登録

```http
POST /documents/
```

指定されたディレクトリのドキュメントを処理し、ベクトルDBに保存します。

リクエストボディ:
```json
{
    "source_path": "path/to/documents",
    "glob_pattern": "**/*[.md|.txt]"  // オプション、デフォルトは "**/*[.md|.txt]"
}
```

### 検索

```http
POST /search/
```

指定されたクエリに基づいて関連ドキュメントを検索します。

リクエストボディ:
```json
{
    "query": "検索クエリ",
    "top_k": 5  // オプション、デフォルトは5
}
```

## エラーハンドリング

- 400: 不正なリクエスト（無効なパス、不正なパラメータなど）
- 500: サーバー内部エラー（RAGCoreの初期化失敗など）

## CORSサポート

すべてのオリジンからのリクエストを許可します（開発用）。本番環境では適切に制限してください。
