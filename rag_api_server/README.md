# RAG API Server (`rag_api_server`)

## 目的

RAG システムのコア機能 (`rag_core`) を利用し、RESTful API として提供する FastAPI サーバーです。他のアプリケーション（例: `mcp_adapter`）が HTTP 経由で RAG 機能を利用できるようにします。

## 現状

-   初期のファイル (`__init__.py`, `main.py`) が作成されました。
-   基本的な FastAPI アプリケーションと `/query` エンドポイントの雛形が `main.py` に記述されています。
-   `rag_core` との連携や、インデックス作成などの他の API エンドポイントの実装はこれから行います。

## 関連コンポーネント

-   `rag_core`: この API サーバーが利用する RAG 機能のコアロジック。
-   `mcp_adapter`: この API サーバーを利用して、RAG 機能を MCP ツールとして提供するアダプター。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../docs/ADR/001-RAG実装の技術選定.md) (FastAPI の選定理由)
