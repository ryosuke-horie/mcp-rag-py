# Progress

## What Works

-   Memory Bank のコアファイル初期化。
-   プロジェクトの基本ディレクトリ構造 (`rag_core`, `rag_api_server`, `mcp_adapter`) の作成。
-   各主要ディレクトリへの `README.md` の配置。
-   `requirements.txt` (依存関係リスト) と `.gitignore` の作成。
-   ディレクトリ構成に関する決定 ([ADR 002](../../docs/ADR/002_モノレポディレクトリ構成.md)) の文書化。

## What's Left to Build

-   DuckDB + VSS 拡張のセットアップ。
-   埋め込みモデル (`pfnet/plamo-embedding-1b`) の準備 (LM Studio 等)。
-   `rag_core` 内の各コンポーネント (document_processor, embedding, vectordb) の実装。
-   `rag_api_server` の API エンドポイント実装と `rag_core` との連携。
-   `mcp_adapter` の MCP サーバーロジック実装 (SDK 選定含む) と `rag_api_server` との連携。

## Current Status

-   プロジェクトの基本的な骨格 (ディレクトリ構造、設定ファイル、ドキュメント) のセットアップ完了。
-   Python 依存関係のインストール完了 (`.venv` 仮想環境を使用)。
-   次のステップは DuckDB + VSS 拡張のセットアップ。

## Known Issues

-   現時点では特になし。

## Evolution of Project Decisions

-   ディレクトリ構成: 初期案から、関心の分離を重視し `rag_core`, `rag_api_server`, `mcp_adapter` に分割する構成に変更 ([ADR 002](../../docs/ADR/002_モノレポディレクトリ構成.md) 参照)。
