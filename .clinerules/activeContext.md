# Active Context

## Current Work Focus

-   `uv` を利用したモノレポ構成への移行完了。
-   `rag_api_server` の動作検証完了済み。
-   プロジェクトルートの `README.md` を `uv` ベースの開発フローに合わせて更新済み。
-   **Dependabot の設定完了 (`uv` エコシステム利用)。**
-   **次のタスク: README.md の本格的なテコ入れ。**

## Recent Changes

-   **開発環境を `pip + venv` から `uv` に移行。**
-   **プロジェクト構成を `uv` ワークスペースを利用したモノレポ構成に変更。**
-   `rag_api_server` の動作検証を実施し、正常動作を確認。
    -   `rag_core/vectordb/storage.py` の型ヒントとデータ処理を修正 (`AttributeError: 'list' object has no attribute 'tolist'` を解決)。
-   プロジェクトルートの `README.md` を更新し、`uv` ベースのセットアップ手順や使い方を詳細化。
-   **Dependabot の設定ファイル (`.github/dependabot.yml`) を作成・更新 (`uv` エコシステム利用)。**

## Next Steps

1.  **README.md の本格的なテコ入れ:**
    -   プロジェクト全体の構成、目的、使い方を明確にする。
    -   各コンポーネント (`rag_core`, `rag_api_server`, `mcp_adapter`) の役割と連携を説明する図を追加する。
    -   開発手順、実行方法、設定項目などを最新化・詳細化する。
    -   必要に応じて、各サブディレクトリの README へのリンクを整理する。
2.  `mcp_adapter` の実装を開始する (`uv` 環境下で)。
