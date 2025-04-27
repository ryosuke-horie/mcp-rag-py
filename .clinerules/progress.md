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

## What's Left to Build

-   `rag_api_server` の API エンドポイント実装：
    - FastAPIアプリケーションの初期設定
    - `rag_core` との連携実装
    - エンドポイントの設計と実装
-   `mcp_adapter` の MCP サーバーロジック実装 (SDK 選定含む) と `rag_api_server` との連携。

## Current Status

-   プロジェクトの基本的な骨格 (ディレクトリ構造、設定ファイル、ドキュメント) のセットアップ完了。
-   Python 依存関係のインストール完了 (`.venv` 仮想環境を使用)。
-   DuckDB + VSS 拡張のセットアップ完了。
-   `rag_core/document_processor` の実装完了（LangChain利用、.txt/.md対応）。
-   `rag_core/embedding` の実装完了（Ollama bge-m3モデル連携）。
-   `rag_core/vectordb` の実装と修正完了：
    - テーブル設計とID管理方法の改善（手動連番管理）
    - VSS拡張の類似度検索関数の正しい使用法確立（array_cosine_similarity）
    - エラーハンドリングの強化
    - 実装知見のドキュメント化
-   次のステップは `rag_api_server` の実装開始。

## Known Issues

-   現時点では特になし。

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

-   ディレクトリ構成: 初期案から、関心の分離を重視し `rag_core`, `rag_api_server`, `mcp_adapter` に分割する構成に変更 ([ADR 002](../../docs/ADR/002_モノレポディレクトリ構成.md) 参照)。
