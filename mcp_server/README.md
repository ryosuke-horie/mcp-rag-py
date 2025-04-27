# MCP Server (`mcp_server`)

## 目的

RAG システムの機能を外部 (例: Cline) から利用可能にするための MCP (Model Context Protocol) サーバーです。FastAPI を使用して RESTful API を提供します。

## 現状

-   初期のファイル (`__init__.py`, `main.py`) が作成されました。
-   基本的な FastAPI アプリケーションの雛形が `main.py` に記述されています。
-   RAG 機能 (ドキュメントのインデックス作成、クエリ処理など) を呼び出す API エンドポイントの実装はこれから行います。

## 関連コンポーネント

-   `rag_core`: このサーバーが提供する RAG 機能のコアロジックを実装しています。`mcp_server` は `rag_core` の各コンポーネント (embedding, vectordb など) を利用します。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../docs/ADR/001-RAG実装の技術選定.md) (FastAPI の選定理由、MCP連携方針)
