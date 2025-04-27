# Tech Context

## 使用技術

- (ここにプロジェクトで使用する主要な技術スタックを記述)
- 例: Python, LangChain, DuckDB, Sentence Transformers

## 開発環境セットアップ

- Python 3.10+ (`.venv` 仮想環境を使用)
- `pip` を使用して `requirements.txt` に記載された依存関係をインストール済み。
- **DuckDB と VSS 拡張:**
    - Python バインディング: `pip install duckdb` (requirements.txt に追加済み想定)
    - VSS 拡張: DuckDB 内から `INSTALL vss; LOAD vss;` を実行してインストール・ロード。
- Ollama (埋め込みモデル用、`bge-m3` を使用)
- 例: Docker (オプション)

## 技術的制約

- (ここにプロジェクトにおける技術的な制約事項を記述)
- 例: ローカル環境での動作、特定のライブラリバージョンの使用

## 依存関係

- `requirements.txt` 参照 (DuckDB を含む)
- DuckDB VSS 拡張 (DuckDB 内部で管理)

## ツール利用パターン

- (ここで開発に使用するツールとその使い方の方針を記述)
- 例: VSCode + Cline, Git for version control
