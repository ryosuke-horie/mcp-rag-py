# Progress

## What Works

-   Memory Bank のコアファイル初期化。
-   **`uv` を利用したモノレポ構成への移行完了:**
    -   プロジェクトの基本ディレクトリ構造 (`src/rag_core`, `src/rag_api_server`, `src/mcp_adapter`) を確立。
    -   各サブプロジェクトに `pyproject.toml` を配置。
    -   ルート `pyproject.toml` で `uv` ワークスペースを定義。
    -   `uv sync` による依存関係管理 (`.venv`, `uv.lock`) を確立。
-   各主要ディレクトリへの `README.md` の配置。
-   `.gitignore` の作成。
-   ディレクトリ構成に関する決定 ([ADR 002](../../docs/ADR/002_モノレポディレクトリ構成.md)) の文書化。
-   DuckDB + VSS 拡張のセットアップ完了。
-   `rag_core/document_processor` (Loader, Splitter) の実装完了 (LangChain 利用、.txt/.md 対応)。
-   `rag_core/embedding` (Ollama API連携) の実装完了 (LangChain 利用、`bge-m3` モデル)。
-   `rag_core/vectordb` (DuckDB+VSS連携) の実装完了。
-   `rag_api_server` の実装完了：
    - FastAPI アプリケーションのセットアップ
    - `rag_core` との連携機能
    - APIエンドポイント（ドキュメント登録、検索）の実装
    - 環境変数ベースの設定管理 (`pydantic-settings`)
    - CORSサポート
    - 実行手順と使用方法のドキュメント化 (`rag_api_server/README.md`)
-   `rag_api_server` の動作検証完了:
    -   `rag_core/vectordb/storage.py` の `AttributeError` を修正。
    -   主要な API エンドポイント (`GET /`, `POST /documents/`, `POST /search/`) の正常動作を確認。
-   **プロジェクトルート `README.md` の更新:**
    -   **`uv` ベースのセットアップ手順、サーバー起動方法 (`uv run`)、API 仕様、使用例、プロジェクト構成図、開発コマンド、ハマりポイントなどを詳細化。**
-   **Dependabot の設定完了 (`uv` エコシステム利用)。**

## What's Left to Build

-   **README.md の本格的なテコ入れ**
-   `mcp_adapter` の MCP サーバーロジック実装:
    - MCPサーバーの基本構造の実装
    - `rag_api_server` との連携機能
    - MCPツールとリソースの定義と実装
    - エラーハンドリングとログ記録
    - 設定管理機能
    - ドキュメントの整備

## Current Status

-   **開発環境が `uv` ベースのモノレポ構成に移行完了。**
-   `rag_api_server` の実装と動作検証が完了:
    -   `uv run` による実行方式を採用。
    -   `uv sync` による仮想環境と依存関係の管理方法を確立。
    -   API の基本機能（ヘルスチェック、ドキュメント登録、検索）が正常に動作。
    -   SwaggerUI (`uv run` で起動) でのAPI確認が可能。
    -   ルート `README.md` に詳細な利用手順を記載済み。
-   **現在のタスクは README.md の本格的なテコ入れ。**
-   次のステップは `mcp_adapter` の実装開始。

## Known Issues

-   現時点では特になし

## DuckDB + VSS 実装の知見

1. テーブル設計とID管理
   - DuckDBの自動採番は独自実装が必要
   - `INTEGER PRIMARY KEY` + アプリケーション側でのID管理が効果的

2. VSS関連の特記事項
   - 類似度検索関数は `array_cosine_similarity` を使用
   - パラメータ化クエリでは明示的な型キャストが必要
   - 配列の次元数指定が必須

3. エラーハンドリング
   - 各操作でのエラーハンドリングが重要
   - トランザクション管理の適切な実装

## Evolution of Project Decisions

-   APIサーバーの実行方式: プロジェクトルートからの実行に決定
    - 相対インポートの問題を解決
    - Pythonのパッケージ構造を正しく認識させる
