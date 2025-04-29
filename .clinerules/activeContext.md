# Active Context

## Current Work Focus

-   `rag_api_server` の動作検証完了:
    -   `rag_core/vectordb/storage.py` の `AttributeError` を修正。
    -   `GET /`, `POST /documents/`, `POST /search/` エンドポイントの正常動作を確認。
-   プロジェクトルートの `README.md` を更新:
    -   セットアップ手順、サーバー起動方法、API仕様、使用例を追記。
-   次のステップとして、`mcp_adapter` の実装を開始する。

## Recent Changes

-   `rag_api_server` の動作検証を実施し、正常動作を確認。
    -   `rag_core/vectordb/storage.py` の型ヒントとデータ処理を修正 (`AttributeError: 'list' object has no attribute 'tolist'` を解決)。
-   プロジェクトルートの `README.md` を更新し、セットアップ手順や使い方を詳細化。

## Next Steps

1.  `mcp_adapter` の実装を開始する:
    -   MCPサーバーのスケルトンコード作成
    -   `rag_api_server` との連携実装
    -   MCPツールとリソースの定義
