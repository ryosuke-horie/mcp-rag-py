# mcp-rag-demo

## DeepWiki

<https://deepwiki.com/ryosuke-horie/mcp-rag-py>

## プロジェクト概要

### 実現したいこと

1. ローカル環境でRAGを構築しMCPで参照できるようにする
2. RAGにプロジェクト固有の情報を溜め込む（チーム固有のルールや規約、利用する技術の公式ドキュメント情報など）
3. Claude等のツールからMCPを経由して情報を呼び出し、生成されるコードに改善が見られるか検証する

 ### 主な機能

 - **ドキュメント登録**:
     - ローカルのドキュメントファイル（`.txt`, `.md`）を読み込み、チャンクに分割。
     - 各チャンクを埋め込みベクトルに変換（Ollama + `bge-m3` モデル使用）。
     - テキストとベクトルをベクトルデータベース（DuckDB + VSS拡張）に保存。
 - **ドキュメント検索**:
     - 自然言語クエリを受け取り、埋め込みベクトルに変換。
     - ベクトルデータベース内で類似度の高いドキュメントチャンクを検索。
 - **MCP連携**:
     - 上記の検索機能をMCPアクションとして公開し、ClaudeなどのLLMツールから利用可能にする。

 ## クイックスタート

 ### 前提条件

| Tool | Version |
|------|---------|
| Python | **3.11 以上 (CPython)** |
| uv | `>=0.6.17` |
| DuckDB 1.2.x | ベクトルDB用 |
| Ollama 0.1.x | 埋め込みモデル用 |

### インストール手順

1. `uv`のインストール

```bash
brew install uv
```

2. 依存関係のインストール

```bash
# プロジェクトルートで実行
uv sync
```

3. 開発サーバーの起動

```bash
uv run uvicorn rag_api_server.main:app --reload
 ```

 ## ドキュメントの登録ワークフロー

 プロジェクト固有の情報（ルール、規約、技術ドキュメントなど）をRAGシステムに登録するには、`rag-core` パッケージに含まれる `rag-core-cli` ツールを使用します。

 ### 手順

 1.  **Ollamaサーバーの起動**:
     ローカルでOllamaサーバーが実行されており、埋め込みモデル（デフォルト: `bge-m3`）が利用可能であることを確認します。
     ```bash
     # (必要であれば) モデルをダウンロードして起動
     ollama run bge-m3
     ```

 2.  **CLIツールの実行**:
     登録したいドキュメントファイルまたはディレクトリを指定して、`rag-core-cli` を実行します。

     **単一ファイルを登録する場合:**
     ```bash
     uv run rag-core-cli --file path/to/your/document.txt
     ```

     **ディレクトリ内の全ファイル（`.txt`, `.md`）を再帰的に登録する場合:**
     ```bash
     uv run rag-core-cli --dir path/to/your/documents/
     ```

     これにより、指定されたドキュメントが処理され、プロジェクトルートにある `vector_store.db` ファイル（ベクトルデータベース）にベクトル情報が保存されます。

 ## プロジェクト構成

```text
mcp-rag/
├─ pyproject.toml               # ルート: uv ワークスペース定義
├─ src/
│  ├─ rag_api_server/           # FastAPI エンドポイント
│  │  ├─ pyproject.toml         #   src-layout / editable
│  │  └─ rag_api_server/…       #   実装
│  ├─ rag_core/                 # RAG ロジック（Embedding, VectorDB）
│  │  ├─ pyproject.toml
│  │  └─ rag_core/…
│  └─ mcp_adapter/              # MCP プロトコルアダプタ
│     └─ …
└─ README.md                    # ← いま見ているファイル
```

### 各コンポーネントの役割

- **`rag_core`**: ドキュメント処理、埋め込み生成、ベクトルDB管理
- **`rag_api_server`**: MCPアクションのバックエンドとして機能するFastAPIサーバー
- **`mcp_adapter`**: MCPプロトコルとの連携

## MCP連携

### Claude Desktopへのインストール

```bash
uv run mcp install src/mcp_adapter/mcp_adapter/server_standalone.py
```

### Ollama モデルの準備

```bash
ollama run bge-m3
```

(初回はモデルのダウンロードが実行されます)

 ### 利用可能なMCPアクション

 - **ドキュメントの検索**: 自然言語クエリに基づいて類似度の高いドキュメントチャンクを検索します。LLMがコンテキストとして利用する情報を取得するために使用されます。
   *(注意: ドキュメントの登録は現在 `rag-core-cli` ツール経由で行います)*

## 開発ガイド

### 開発時のコマンドメモ

| タスク | コマンド |
|--------|---------|
| 依存追加 | `uv pip install -e src/rag_core[dev]` |
| Lint / Format | `uv run ruff check .` , `uv run ruff format .` |
| テスト | `uv run pytest` |
| 仮想環境を捨てる | `rm -rf .venv uv.lock` |
