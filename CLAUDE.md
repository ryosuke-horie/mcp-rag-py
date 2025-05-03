# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language / 言語設定
- 日本語でのレスポンスを優先してください。技術的な用語は英語のままで構いません。
- Please respond in Japanese. Technical terms can remain in English.

## Build/Test/Lint Commands / ビルド・テスト・リントコマンド
- 依存関係のインストール: `uv sync`
- 開発サーバーの起動: `uv run uvicorn rag_api_server.main:app --reload`
- リント: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- テスト実行: `uv run pytest`
- 単一テスト実行: `uv run pytest path/to/test.py::test_function_name -v`
- CLIツール使用: `uv run rag-core-cli --file path/to/file.txt` または `--dir path/to/dir/`
- MCPアダプターのインストール: `uv run mcp install src/mcp_adapter/mcp_adapter/server_standalone.py`
- Ollamaサーバーの起動: `ollama run bge-m3`

## Code Style Guidelines / コードスタイルガイドライン
- Python: 3.11以上が必要
- 行の長さ: 最大88文字
- インポート: `ruff`のインポート順序（isort）を使用
- エラー処理: 例外連鎖には `raise ... from` を優先
- 命名規則: PEP8規約に従う（変数/関数にはsnake_case）
- プロジェクト構造: src-layoutと編集可能なインストールを使用
- 型アノテーション: 関数のシグネチャと戻り値には型アノテーションを推奨
- ドキュメンテーション: モジュール、クラス、公開関数にはドキュメント文字列を記述

## Project Structure / プロジェクト構造
- `rag_core/`: RAGシステムのコアロジック（ドキュメント処理、埋め込み、ベクトルDB）
- `rag_api_server/`: RAG機能を提供するFastAPIサーバー
- `mcp_adapter/`: MCPプロトコルアダプターとツール実装

## Available MCP Tools / 利用可能なMCPツール
- `search_documents(query: str, top_k: int = 5)`: ドキュメント検索
- `add_document(content: str, title: Optional[str] = None)`: ドキュメント追加
- `check_rag_status()`: RAGシステムのステータス確認

## Requirements / 必要環境
- Python 3.11+
- DuckDB 1.2.x (ベクトルDB用)
- Ollama 0.1.x (埋め込みモデル用)
- uv パッケージマネージャー