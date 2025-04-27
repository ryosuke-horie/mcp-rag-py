# Active Context

## Current Work Focus

-   Python 依存関係のインストール完了 (`.venv` 仮想環境を使用)。
-   次のステップとして、DuckDB + VSS 拡張のセットアップ方法を確認・実施する。
-   引き続き、開発環境セットアップを進める（埋め込みモデル準備）。

## Recent Changes

-   Memory Bank のコアファイル (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`, `activeContext.md`) の初期バージョンを作成。
-   プロジェクトのディレクトリ構造を定義し、関連ファイル (`__init__.py`, `README.md` 等) を作成 ([ADR 002](../../docs/ADR/002_モノレポディレクトリ構成.md) 参照)。
    -   `rag_core` (コアロジック)
    -   `rag_api_server` (FastAPI サーバー雛形)
    -   `mcp_adapter` (MCP アダプター雛形)
-   `requirements.txt` と `.gitignore` を作成。
-   ADR 002 を作成し、ディレクトリ構成の決定を記録。
-   Python 依存関係を `.venv` 仮想環境にインストール (`requirements.txt` に基づく)。

## Next Steps

1.  DuckDB + VSS 拡張のセットアップ方法を確認・実施する。
2.  LM Studio 等で埋め込みモデル (`pfnet/plamo-embedding-1b`) を利用可能にする手順を確認・実施する。
3.  各コンポーネント (`rag_core`, `rag_api_server`, `mcp_adapter`) の実装を開始する。
