# mcp-rag-demo

## 実現したいこと

1. ローカル環境でRAGを構築しMCPで参照できるようにする
2. RAGにプロジェクト固有の情報を溜め込む（チーム固有のルールや規約、利用する技術の公式ドキュメント情報など）
3. Claude等のツールからMCPを経由して情報を呼び出し、生成されるコードに改善が見られるか検証する

## セットアップ手順

### 1. 前提条件

*   Python 3.10 以降
*   [Ollama](https://ollama.com/) がインストールされていること

### 2. 仮想環境の作成と有効化

プロジェクトルートで以下のコマンドを実行します。

```bash
# 仮想環境を作成 (初回のみ)
python -m venv .venv

# 仮想環境を有効化 (fishシェルの場合)
source .venv/bin/activate.fish
# (bash/zsh の場合は source .venv/bin/activate)
```

### 3. 依存関係のインストール

仮想環境を有効化した状態で、以下のコマンドを実行します。

```bash
pip install -r requirements.txt
```

### 4. Ollama モデルの準備

RAG システムで使用する埋め込みモデル (`bge-m3`) を Ollama で利用可能にします。

```bash
ollama run bge-m3
```
(初回はモデルのダウンロードが実行されます)

### 5. (オプション) 環境変数による設定

API サーバーは環境変数で設定を上書きできます。必要に応じて `.env` ファイルを作成するか、環境変数を設定してください。主な設定項目は以下の通りです (デフォルト値は `rag_api_server/config.py` 参照)。

*   `OLLAMA_BASE_URL`: Ollama サーバーの URL (デフォルト: `http://localhost:11434`)
*   `EMBEDDING_MODEL_NAME`: 使用する埋め込みモデル名 (デフォルト: `bge-m3`)
*   `DB_PATH`: DuckDB データベースファイルのパス (デフォルト: `vector_store.db`)
*   `TABLE_NAME`: ベクトルストアのテーブル名 (デフォルト: `embeddings`)

## RAG API サーバーの起動

仮想環境を有効化した状態で、プロジェクトルートから以下のコマンドを実行します。

```bash
uvicorn rag_api_server.main:app --reload --port 8001
```

*   `--reload`: コード変更時にサーバーを自動再起動します。
*   `--port 8001`: サーバーがリッスンするポートを指定します (デフォルトは 8000 ですが、環境に合わせて変更可能です)。

サーバーが正常に起動すると、`Uvicorn running on http://127.0.0.1:8001` のようなログが表示されます。

## 利用可能な機能 (API エンドポイント)

API サーバーは以下のエンドポイントを提供します。Swagger UI (`http://127.0.0.1:8001/docs`) からも確認・試用できます。

*   **`GET /`**:
    *   **説明:** API サーバーのヘルスチェック。
    *   **レスポンス:** `{"status": "healthy", "version": "サーバーバージョン"}`
*   **`POST /documents/`**:
    *   **説明:** 指定されたディレクトリ内のドキュメント (.txt, .md) を処理し、チャンク分割、埋め込みベクトル生成を行い、ベクトルデータベースに保存します。
    *   **リクエストボディ:** `{"source_path": "処理対象ディレクトリのパス", "glob_pattern": "ファイルパターン (オプション, デフォルト: **/*[.md|.txt])"}`
    *   **レスポンス (成功時):** `{"status": "success", "processed_documents": 数, "processed_chunks": 数, "message": "..."}`
    *   **レスポンス (失敗時):** `{"detail": "エラーメッセージ"}`
*   **`POST /search/`**:
    *   **説明:** 指定されたクエリに基づいて、ベクトルデータベースから類似度の高いドキュメントチャンクを検索します。
    *   **リクエストボディ:** `{"query": "検索クエリ文字列", "top_k": 取得件数 (オプション, デフォルト: 5)}`
    *   **レスポンス (成功時):** `{"results": [{"text": "チャンクテキスト", "similarity": 類似度スコア}, ...]}`
    *   **レスポンス (失敗時):** `{"detail": "エラーメッセージ"}`

## 使い方 (curl 例)

### ヘルスチェック

```bash
curl http://127.0.0.1:8001/
```

### ドキュメントの登録

プロジェクト内の `docs` ディレクトリを登録する場合:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"source_path": "docs"}' \
     http://127.0.0.1:8001/documents/
```

### ドキュメントの検索

"DuckDB" というクエリで上位 3 件を検索する場合:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"query": "DuckDB", "top_k": 3}' \
     http://127.0.0.1:8001/search/
```
