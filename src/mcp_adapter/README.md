# MCP Adapter for RAG System

このパッケージは、MCP（Model Context Protocol）サーバーを提供し、RAG APIサーバーと連携してClineなどのAIアシスタントから利用できるようにします。

## 機能

- MCP（Model Context Protocol）サーバーの実装
- RAG APIサーバーとの連携
- ドキュメント検索機能
- ドキュメント追加機能
- システムステータス確認機能

## インストール

プロジェクトルートから以下のコマンドを実行します：

```bash
uv sync
```

## 実行方法

プロジェクトルートから以下のコマンドを実行します：

```bash
# 開発モード
uv run -m mcp_adapter

# Claude Desktopへのインストール（MCPサーバーとして登録）
uv run -m mcp rag install src/mcp_adapter/mcp_adapter/main.py
```

## 環境変数

以下の環境変数を設定することで、MCPアダプターの動作をカスタマイズできます：

- `MCP_ADAPTER_SERVER_NAME`: MCPサーバーの名前（デフォルト: "RAG MCP Adapter"）
- `MCP_ADAPTER_RAG_API_BASE_URL`: RAG APIサーバーのベースURL（デフォルト: "http://localhost:8000"）
- `MCP_ADAPTER_HOST`: ホスト名（デフォルト: "localhost"）
- `MCP_ADAPTER_PORT`: ポート番号（デフォルト: 8080）
- `MCP_ADAPTER_LOG_LEVEL`: ログレベル（デフォルト: "info"）

## ツールとリソース

### ツール

- `search_documents(query: str, top_k: int = 5)`: ドキュメントを検索します
- `add_document(content: str, title: Optional[str] = None)`: 新しいドキュメントを追加します
- `check_rag_status()`: RAG APIサーバーのステータスを確認します

### リソース

- `rag-info://status`: RAGシステムのステータス情報を取得します

## Clineでの使用例

```
@search_documents クエリ: "DuckDBとは何ですか"
```

```
@add_document コンテンツ: "DuckDBは、分析処理に最適化された組み込み型カラム指向データベースです。SQLiteのように簡単に使えますが、分析クエリに対してはずっと高速です。" タイトル: "DuckDBの概要"
```

```
@check_rag_status
```
