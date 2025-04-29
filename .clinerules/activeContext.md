# Active Context

## Current Work Focus

-   `uv` を利用したモノレポ構成への移行完了。
-   `rag_api_server` の動作検証完了済み。
-   プロジェクトルートの `README.md` を `uv` ベースの開発フローに合わせて更新済み。
-   次のステップとして、`mcp_adapter` の実装を開始する (`uv` 環境下で)。

## Recent Changes

-   **開発環境を `pip + venv` から `uv` に移行。**
-   **プロジェクト構成を `uv` ワークスペースを利用したモノレポ構成に変更。**
-   `rag_api_server` の動作検証を実施し、正常動作を確認。
    -   `rag_core/vectordb/storage.py` の型ヒントとデータ処理を修正 (`AttributeError: 'list' object has no attribute 'tolist'` を解決)。
-   プロジェクトルートの `README.md` を更新し、`uv` ベースのセットアップ手順や使い方を詳細化。

## Next Steps

1.  `mcp_adapter` の実装を開始する:
    -   MCPサーバーのスケルトンコード作成
    -   `rag_api_server` との連携実装
    -   MCPツールとリソースの定義
