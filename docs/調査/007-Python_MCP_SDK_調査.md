# Python Model Context Protocol (MCP) SDK 調査

## 概要

Model Context Protocol (MCP) は、LLMアプリケーションが安全かつ標準化された方法で外部のデータや機能（ツール、リソース）にアクセスするためのオープンプロトコルです。Anthropic社が主導しています。

Python MCP SDK は、MCPサーバーおよびクライアントをPythonで開発するための公式ライブラリです。これにより、開発者は独自のMCPサーバーを構築し、LLM（例: Claude）や対応クライアント（例: Cursor）から利用可能なツールやリソースを提供できます。

**主な情報源:**

*   **公式GitHubリポジトリ:** [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
*   **MCP公式サイト (サーバー開発者向け):** [https://modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)
*   **MCP公式サイト (クライアント開発者向け):** [https://modelcontextprotocol.io/quickstart/client](https://modelcontextprotocol.io/quickstart/client)
*   **Anthropicによる紹介記事:** [https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)
*   **DataCampチュートリアル:** [https://www.datacamp.com/tutorial/mcp-model-context-protocol](https://www.datacamp.com/tutorial/mcp-model-context-protocol)

## インストール

```bash
pip install modelcontextprotocol
```

## サーバー開発

### 基本的な構造

MCPサーバーは、`modelcontextprotocol.server.mcp.McpServer` クラスをインスタンス化して作成します。サーバーには名前とバージョンを指定します。ツールやリソースは、このサーバーインスタンスに登録していきます。

```python
import asyncio
from modelcontextprotocol.server.mcp import McpServer
from modelcontextprotocol.server.stdio import StdioServerTransport
from modelcontextprotocol.server.tools import Tool, ToolParameter, ToolResult

# サーバーインスタンスの作成
server = McpServer(name="my-rag-mcp-server", version="0.1.0")

# (ここにツールやリソースの定義と登録を追加)

# サーバーの実行 (例: 標準入出力トランスポートを使用)
async def main():
    transport = StdioServerTransport(server)
    await transport.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### ツール (Tools) の定義

ツールは `modelcontextprotocol.server.tools.Tool` クラスを使用して定義します。ツールには名前、説明、入力パラメータ、そして実行される関数（ハンドラー）を指定します。入力パラメータは `ToolParameter` で定義します。

```python
from pydantic import BaseModel, Field

# ツールの入力パラメータを定義する Pydantic モデル
class SearchInput(BaseModel):
    query: str = Field(..., description="検索クエリ")
    top_k: int = Field(default=3, description="取得する検索結果の数")

# ツールを実行する非同期関数 (ハンドラー)
async def handle_search(params: SearchInput) -> ToolResult:
    # ここで rag_api_server の検索エンドポイントを呼び出すなどの処理を行う
    print(f"Searching for: {params.query} (top_k={params.top_k})")
    # ダミーの検索結果
    results = [
        {"title": "Result 1", "content": "Content for result 1..."},
        {"title": "Result 2", "content": "Content for result 2..."},
    ]
    # ToolResult を返す (content は通常 JSON 文字列など)
    return ToolResult(content=str(results)) # Pydantic モデルを .model_dump_json() するのが一般的

# ツールインスタンスの作成
search_tool = Tool(
    name="rag_search",
    description="RAGシステムを使用してドキュメントを検索します。",
    input_schema=SearchInput.model_json_schema(), # Pydantic モデルからスキーマを生成
    handler=handle_search,
)

# サーバーにツールを登録
server.add_tool(search_tool)
```
入力スキーマは Pydantic モデルを使用して定義するのが一般的で、`model_json_schema()` メソッドで JSON Schema を取得して渡します。ハンドラー関数は非同期 (`async def`) で定義し、入力パラメータに対応する Pydantic モデルのインスタンスを受け取り、`ToolResult` を返す必要があります。

### リソース (Resources) の定義

リソースは、LLM がコンテキストとして参照できるデータを提供します。`modelcontextprotocol.server.roots.Root` や `modelcontextprotocol.server.resources.Resource` を使って定義できますが、現時点 (SDK v1.x) ではツールの利用が主であり、リソースの具体的な利用例はまだ少ないようです。

基本的な考え方としては、特定の URI に対応するデータを返すハンドラーを定義します。

```python
from modelcontextprotocol.server.resources import Resource, ResourceResult
from modelcontextprotocol.server.roots import Root

# ダミーのリソースハンドラー
async def get_document_content(uri: str) -> ResourceResult:
    # URIに基づいてドキュメント内容を取得する処理 (例)
    print(f"Fetching resource for URI: {uri}")
    if uri == "mcp://my-rag-mcp-server/documents/doc1":
        return ResourceResult(content="これはドキュメント1の内容です。", content_type="text/plain")
    else:
        # 見つからない場合は None または空の ResourceResult を返す
        return ResourceResult(content=None) # または raise NotFoundError

# リソースを定義 (より複雑な構造は Root を使う)
# 単純なリソースの例 (直接 Resource を使うのは稀かもしれない)
# doc_resource = Resource(uri="mcp://my-rag-mcp-server/documents/doc1", handler=get_document_content)
# server.add_resource(doc_resource) # McpServer に直接 Resource を追加するメソッドはなさそう

# Root を使ってリソース階層を定義する例
class DocumentRoot(Root):
    async def get_resource(self, uri: str) -> ResourceResult | None:
        # この Root が担当する URI かどうかをチェック
        if uri.startswith("mcp://my-rag-mcp-server/documents/"):
            return await get_document_content(uri)
        return None # 担当外なら None

# サーバーに Root を登録
server.add_root(DocumentRoot())

```
リソースへのアクセスは URI (`mcp://<server_name>/<path>`) を通じて行われます。サーバーは登録された Root や Resource の中から、指定された URI にマッチするハンドラーを探して実行します。

### サーバーの起動

サーバーはトランスポート (`Transport`) を介してクライアントと通信します。最も一般的なのは標準入出力 (`StdioServerTransport`) を使用する方法です。

```python
import asyncio
from modelcontextprotocol.server.mcp import McpServer
from modelcontextprotocol.server.stdio import StdioServerTransport
# (ツールやリソースの定義...)

server = McpServer(name="my-rag-mcp-server", version="0.1.0")
# server.add_tool(...)
# server.add_root(...)

async def main():
    # 標準入出力を介して通信するトランスポートを作成
    transport = StdioServerTransport(server)
    print("MCP Server starting on stdio...")
    # サーバーを実行 (クライアントからの接続を待機)
    await transport.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("MCP Server stopped.")
```
このコードを実行すると、サーバーは標準入力からのリクエストを待ち受け、標準出力に応答を返します。VS Code のようなクライアントは、このプロセスをバックグラウンドで実行し、標準入出力を介して通信します。

## クライアントからの利用 (参考)

Python SDK にはクライアント機能 (`modelcontextprotocol.client`) も含まれており、他の MCP サーバーに接続してツールやリソースを利用できます。

```python
import asyncio
from modelcontextprotocol.client.mcp import McpClient
from modelcontextprotocol.client.stdio import StdioClientTransport

async def run_client():
    # サーバープロセスを起動するコマンド
    server_command = ["python", "path/to/your/server_main.py"] # サーバーの起動スクリプトを指定

    # Stdio トランスポートでクライアントを作成
    transport = StdioClientTransport(server_command)
    client = McpClient(transport)

    try:
        # サーバーに接続
        await client.start()
        print(f"Connected to server: {client.server_info}")

        # サーバーのツール 'rag_search' を呼び出す
        tool_name = "rag_search"
        params = {"query": "What is MCP?", "top_k": 2}

        print(f"Calling tool '{tool_name}' with params: {params}")
        result = await client.call_tool(tool_name, params)
        print(f"Tool result: {result.content}")

        # リソースを取得 (例)
        # resource_uri = "mcp://my-rag-mcp-server/documents/doc1"
        # resource_content = await client.get_resource(resource_uri)
        # print(f"Resource content: {resource_content}")

    finally:
        # サーバーとの接続を閉じる
        await client.stop()
        print("Disconnected from server.")

if __name__ == "__main__":
    asyncio.run(run_client())
```
クライアントは、サーバープロセスを起動し、標準入出力を介して通信します (`StdioClientTransport`)。`client.call_tool()` でツールを呼び出し、`client.get_resource()` でリソースを取得できます。

## 注意点

*   **SDKバージョン:** サーバー開発には Python MCP SDK `1.2.0` 以上が必要です (公式サイト情報)。
*   **セキュリティ:** MCPは安全な接続を目指していますが、サーバー実装者は認証や認可、入力値の検証などを適切に行う必要があります。
*   **非同期処理:** SDKは非同期 (`asyncio`) をサポートしている可能性があります。サーバーの実装によっては考慮が必要です。

## 公開時のベストプラクティス

*   **ドキュメント:** 提供するツールやリソースの名前、説明、入力スキーマ、出力形式、利用例などを明確に文書化します。README や Docstring を活用しましょう。
*   **エラーハンドリング:** 堅牢なエラーハンドリングを実装する。
*   **バージョニング:** サーバー名 (`name`) に加えて `version` を指定し、変更があった場合にインクリメントします。互換性のない変更にはメジャーバージョンを上げます。
*   **テスト:** 各ツールのハンドラー関数やリソース取得ロジックに対して単体テストや結合テストを作成し、動作を保証します。
*   **設定管理:** APIキーやデータベース接続情報など、外部設定は環境変数や設定ファイルから読み込むようにします。
*   **ロギング:** サーバーの動作状況やエラーを記録するために、適切なロギングを実装します。
*   **依存関係:** `requirements.txt` や `pyproject.toml` で依存関係を明確に管理します。

## まとめ

Python MCP SDK は、MCPサーバーを構築するための重要なツールです。公式ドキュメントやGitHubリポジトリの例を参照しながら、ツールやリソースを定義し、サーバーを実装していく必要があります。セキュリティやエラーハンドリングにも注意が必要です。
