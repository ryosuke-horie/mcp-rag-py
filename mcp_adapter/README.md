# MCP Adapter (`mcp_adapter`)

## 目的

このパッケージは、`rag_api_server` が提供する RAG 機能を MCP (Model Context Protocol) に適合させるためのアダプターとして機能します。MCP ホスト (例: Cline) からのツール実行リクエストを受け取り、それを `rag_api_server` への HTTP リクエストに変換し、結果を MCP ホストに返します。

## 実装概要

-   **Python MCP SDK (`modelcontextprotocol`)** を使用して実装されています。
-   `mcp_spec.py`:
    -   提供する MCP ツール `query_rag_system` を `Tool` クラスと Pydantic モデル (`QueryRagInput`) を使用して定義しています。
    -   入力として `query` (必須) と `top_k` (オプション、デフォルト5) を受け付けます。
-   `client.py`:
    -   `requests` ライブラリを使用して `rag_api_server` の `/search/` エンドポイントを呼び出す `query_rag_api` 関数を提供します。
    -   APIサーバーのURLは環境変数 `RAG_API_URL` で設定可能 (デフォルト: `http://127.0.0.1:8000`)。
-   `main.py`:
    -   `McpServer` と `StdioServerTransport` を使用して MCP サーバーをセットアップします。
    -   `query_rag_system` ツールの非同期ハンドラー (`handle_query_rag_system`) を定義し、`client.py` の関数を呼び出して結果を `ToolResult` として返します。
    -   標準入出力を介して MCP ホストと通信します。

## セットアップと実行

1.  **依存関係のインストール:**
    プロジェクトルートディレクトリで、仮想環境を有効にした後、必要なライブラリをインストールします。
    ```bash
    pip install -r requirements.txt
    ```
    (`requests` と `modelcontextprotocol` が `requirements.txt` に含まれていることを確認してください。)

2.  **RAG API サーバーの起動:**
    `mcp_adapter` を使用する前に、`rag_api_server` が起動している必要があります。プロジェクトルートから以下のコマンドを実行します。
    ```bash
    uvicorn rag_api_server.main:app --reload --host 0.0.0.0 --port 8000
    ```
    (必要に応じてホストやポートを変更してください。`RAG_API_URL` 環境変数を設定している場合は、それに合わせてください。)

3.  **MCP Adapter サーバーの起動:**
    MCP ホスト (例: Cline, Cursor) がこのアダプターを利用できるように、以下のコマンドでサーバーを起動します。通常、MCPホスト側がこのコマンドを実行します。
    ```bash
    python -m mcp_adapter.main
    ```
    これにより、サーバーは標準入出力を介してリクエストを待ち受けます。

## 関連コンポーネント

-   `rag_api_server`: このアダプターが HTTP 経由で呼び出す、実際の RAG 機能を提供する API サーバー。
-   MCP Host (外部): このアダプターが提供するツールを利用するクライアント (例: Cline)。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../docs/ADR/001-RAG実装の技術選定.md) (MCP連携方針の背景)
