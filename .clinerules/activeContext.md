# Active Context

## Current Work Focus

-   `rag_core/vectordb` (DuckDB+VSS連携) の実装完了。
-   次のステップとして、`rag_api_server` の実装を開始する。

## Recent Changes

-   Memory Bank のコアファイル (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`, `activeContext.md`) の初期バージョンを作成。
-   プロジェクトのディレクトリ構造を定義し、関連ファイル (`__init__.py`, `README.md` 等) を作成 ([ADR 002](../../docs/ADR/002_モノレポディレクトリ構成.md) 参照)。
    -   `rag_core` (コアロジック)
    -   `rag_api_server` (FastAPI サーバー雛形)
    -   `mcp_adapter` (MCP アダプター雛形)
-   `requirements.txt` と `.gitignore` を作成。
-   ADR 002 を作成し、ディレクトリ構成の決定を記録。
-   Python 依存関係を `.venv` 仮想環境にインストール (`requirements.txt` に基づく)。
-   `rag_core/document_processor` の Loader (`loader.py`) と Splitter (`splitter.py`) を LangChain を利用して実装。`.txt` と `.md` ファイルに対応。
-   `rag_core/embedding` の Model (`model.py`) を LangChain (`langchain-ollama`) を利用して実装。Ollama (`bge-m3`) と連携。
-   `rag_core/vectordb` の Storage (`storage.py`) を DuckDB+VSS を利用して実装。

## Next Steps

1.  Ollama で埋め込みモデル（`bge-m3`）を利用可能にする手順を確認・実施する。（完了）
2.  `rag_core` コンポーネントの実装を進める。
    -   `rag_core/document_processor` (Loader, Splitter) - **完了**
    -   `rag_core/embedding` (Ollama API連携) - **完了**
    -   `rag_core/vectordb` (DuckDB+VSS連携) - **完了**
3.  `rag_api_server` の実装。 - **着手**
4.  `mcp_adapter` の実装。
