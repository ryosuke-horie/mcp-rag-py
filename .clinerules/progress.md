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
    - 実行手順と使用方法のドキュメント化 (`rag_api_server/README.md`)
-   `rag_api_server` の動作検証完了:
    -   `rag_core/vectordb/storage.py` の `AttributeError` を修正。
    -   主要な API エンドポイント (`GET /`, `POST /documents/`, `POST /search/`) の正常動作を確認。
-   プロジェクトルート `README.md` の更新:
    -   セットアップ手順、サーバー起動方法、API 仕様、使用例を追記。
-   `mcp_adapter` の実装完了:
    -   Python MCP SDK (`modelcontextprotocol`) を使用。
    -   `requirements.txt` に依存関係 (`requests`, `modelcontextprotocol`) を追加。
    -   `mcp_spec.py` を SDK の `Tool` クラスと Pydantic モデルで更新。
    -   `client.py` の API エンドポイントを `/search/` に修正。
    -   `main.py` に SDK ベースのサーバーロジックとツールハンドラーを実装。
    -   `README.md` に実装詳細と実行手順を更新。

## What's Left to Build

-   `mcp_adapter` のテスト実装 (単体テスト、結合テスト)。
-   `rag_api_server` と `mcp_adapter` を連携させたエンドツーエンドテスト。
-   必要に応じて `mcp_adapter` にドキュメントインデックス用ツールの追加。
-   Memory Bank の継続的な更新。

## Current Status

-   `rag_api_server` の実装と動作検証が完了。
-   `mcp_adapter` の実装が完了し、Python MCP SDK を使用して `rag_api_server` の機能を MCP ツールとして公開。
-   次のステップは、実装された `mcp_adapter` のテスト。

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
