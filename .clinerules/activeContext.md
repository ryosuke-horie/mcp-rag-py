# Active Context

## Current Work Focus

-   `mcp_adapter` の実装完了。
-   次のステップとして、実装された `mcp_adapter` のテストを行う。

## Recent Changes

-   `mcp_adapter` を Python MCP SDK (`modelcontextprotocol`) を使用して実装。
    -   `requirements.txt` に依存関係 (`requests`, `modelcontextprotocol`) を追加。
    -   `mcp_spec.py` を SDK の `Tool` クラスと Pydantic モデルで更新。
    -   `client.py` の API エンドポイントを `/search/` に修正。
    -   `main.py` に SDK ベースのサーバーロジックとツールハンドラーを実装。
    -   `README.md` に実装詳細と実行手順を更新。
-   `rag_api_server` の問い合わせエンドポイントが `/search/` であることを確認。
-   Memory Bank (`progress.md`, `activeContext.md`) を更新。

## Next Steps

1.  `mcp_adapter` のテスト実装を開始する:
    -   単体テスト (各コンポーネント、特にハンドラーロジック)。
    -   結合テスト (`mcp_adapter` と `rag_api_server` の連携)。
    -   エンドツーエンドテスト (MCPクライアントからのツール呼び出し)。
2.  必要に応じて `mcp_adapter` にドキュメントインデックス用ツールの追加を検討する。
3.  Memory Bank の継続的な更新。
