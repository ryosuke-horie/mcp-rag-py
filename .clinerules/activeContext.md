# Active Context

## Current Work Focus

-   **uv の調査:** Brave 検索と Playwright を利用して、Python 初心者向けに `uv` のインストール、利用方法、`venv` との違い、注意点などを調査する。
-   `mcp_adapter` のテスト実装 (uv 調査完了後)。

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

1.  **uv の調査:**
    -   Brave 検索で関連情報を収集する (インストール、チュートリアル、venv との比較、ベストプラクティス)。
    -   Playwright で収集したページの情報を分析・整理する。
    -   調査結果をまとめる。
2.  **uv への移行 (調査結果による):**
    -   プロジェクトの仮想環境を `venv` から `uv` に移行する。
3.  **`mcp_adapter` のテスト実装:**
    -   単体テスト、結合テスト、エンドツーエンドテストを実装する。
4.  必要に応じて `mcp_adapter` にドキュメントインデックス用ツールの追加を検討する。
5.  Memory Bank の継続的な更新。
