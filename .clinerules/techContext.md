# Tech Context

## 使用技術

- (ここにプロジェクトで使用する主要な技術スタックを記述)
- 例: Python, LangChain, DuckDB, Sentence Transformers

## 開発環境セットアップ

- Python 3.11+ (CPython)
- `uv` (>=0.6.17) を使用して依存関係を管理 (`uv sync` で `.venv` を生成・同期)。
- **DuckDB と VSS 拡張:**
    - Python バインディング: `uv sync` によりインストールされる (各サブプロジェクトの `pyproject.toml` で定義)。
    - VSS 拡張: DuckDB 内から `INSTALL vss; LOAD vss;` を実行してインストール・ロード。
- Ollama (埋め込みモデル用、`bge-m3` を使用)

## 技術的制約

- (ここにプロジェクトにおける技術的な制約事項を記述)
- 例: ローカル環境での動作、特定のライブラリバージョンの使用

## 依存関係

- 各サブプロジェクト (`src/*`) の `pyproject.toml` で定義。
- ルートの `pyproject.toml` でワークスペース (`[tool.uv.workspace]`) を定義し、`uv sync` で管理。
- `uv.lock` ファイルで依存関係のバージョンを固定。
- DuckDB VSS 拡張 (DuckDB 内部で管理)

## ツール利用パターン

- VSCode + Cline
- Git for version control
- `uv` for dependency management and task running (`uv run`)
- GitHub Actions (CI用)
- Dependabot (依存関係更新用)
