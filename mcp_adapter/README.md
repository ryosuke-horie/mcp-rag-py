# MCP Adapter (`mcp_adapter`)

## 目的

このパッケージは、`rag_api_server` が提供する RAG 機能を MCP (Model Context Protocol) に適合させるためのアダプターとして機能します。MCP ホスト (例: Cline) からのツール実行リクエストを受け取り、それを `rag_api_server` への HTTP リクエストに変換し、結果を MCP ホストに返します。

## 現状

-   初期のファイル (`__init__.py`, `mcp_spec.py`, `client.py`, `main.py`) が作成されました。
-   `mcp_spec.py`: 提供する MCP ツール (`query_rag_system`) を定義しています。
-   `client.py`: `rag_api_server` の `/query` エンドポイントを呼び出す基本的なクライアントロジックが含まれています。
-   `main.py`: MCP ツール実行リクエストを受け取り、`client.py` を介して `rag_api_server` を呼び出す処理の骨格が記述されています。実際の MCP サーバーとしての実行は、使用する MCP SDK やフレームワークに依存します。

## 関連コンポーネント

-   `rag_api_server`: このアダプターが HTTP 経由で呼び出す、実際の RAG 機能を提供する API サーバー。
-   MCP Host (外部): このアダプターが提供するツールを利用するクライアント (例: Cline)。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../docs/ADR/001-RAG実装の技術選定.md) (MCP連携方針の背景)
