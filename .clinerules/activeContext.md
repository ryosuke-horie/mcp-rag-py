# Active Context

## Current Work Focus

-   `uv` を利用したモノレポ構成への移行完了。
-   `rag_api_server` の動作検証完了済み。
-   プロジェクトルートの `README.md` を `uv` ベースの開発フローに合わせて更新済み。
-   **CI/CD (GitHub Actions) と Dependabot の設定。**

## Recent Changes

-   **開発環境を `pip + venv` から `uv` に移行。**
-   **プロジェクト構成を `uv` ワークスペースを利用したモノレポ構成に変更。**
-   `rag_api_server` の動作検証を実施し、正常動作を確認。
    -   `rag_core/vectordb/storage.py` の型ヒントとデータ処理を修正 (`AttributeError: 'list' object has no attribute 'tolist'` を解決)。
-   プロジェクトルートの `README.md` を更新し、`uv` ベースのセットアップ手順や使い方を詳細化。

## Next Steps

1.  **CI (GitHub Actions) の設定:**
    -   `.github/workflows/ci.yml` を作成。
    -   `push` (main) および `pull_request` トリガーを設定。
    -   Python 3.11, `uv` のセットアップジョブを定義。
    -   `uv sync` による依存関係インストールステップを追加。
    -   `pre-commit run --all-files` によるリンター/フォーマッター実行ステップを追加。
2.  **Dependabot の設定:**
    -   `.github/dependabot.yml` を作成。
    -   `pip` (ルートおよびサブプロジェクト) と `github-actions` のエコシステムを設定。
    -   更新スケジュールを `daily` に設定。
3.  `mcp_adapter` の実装を開始する (`uv` 環境下で)。
