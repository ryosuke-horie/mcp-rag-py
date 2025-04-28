# Progress

## What Works

-   Memory Bank のコアファイル初期化。
-   プロジェクトの基本ディレクトリ構造 (`rag_core`, `rag_api_server`, `mcp_adapter`) の作成。
-   各主要ディレクトリへの `README.md` の配置。
-   `requirements.txt` (依存関係リスト) と `.gitignore` の作成。
-   ディレクトリ構成に関する決定 ([ADR 002](../../docs/ADR/002_モノレポディレクトリ構成.md)) の文書化。
-   Python 依存関係のインストール完了 (`.venv` 仮想環境を使用)。
-   DuckDB + VSS 拡張のセットアップ完了。
-   `rag_core/document_processor` (Loader, Splitter) の実装完了 (LangChain 利用、.txt/.md 対応)。
-   `rag_core/embedding` (Ollama API連携) の実装完了 (LangChain 利用、`bge-m3` モデル)。
-   `rag_core/vectordb` (DuckDB+VSS連携) の実装完了。
-   `rag_api_server` の実装完了：
    - FastAPI アプリケーションのセットアップ
    - `rag_core` との連携機能
    - APIエンドポイント（ドキュメント登録、検索）の実装
    - 環境変数ベースの設定管理
    - CORSサポート
    - 実行手順と使用方法のドキュメント化

## What's Left to Build

-   `mcp_adapter` の MCP サーバーロジック実装:
    - MCPサーバーの基本構造の実装
    - `rag_api_server` との連携機能
    - MCPツールとリソースの定義と実装
    - エラーハンドリングとログ記録
    - 設定管理機能
    - ドキュメントの整備

## Current Status

-   `rag_api_server` の実装が完了し、動作確認済み：
    - プロジェクトルートからの実行方式を採用
    - 仮想環境と依存関係の管理方法を確立
    - API の基本機能（ヘルスチェック、ドキュメント登録、検索）が動作
    - SwaggerUI でのAPI確認が可能
-   次のステップは `mcp_adapter` の実装開始

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
