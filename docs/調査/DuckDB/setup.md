# DuckDB + VSS 拡張 セットアップ (Python)

Python 環境で DuckDB と VSS 拡張をセットアップする手順です。

## 1. DuckDB ライブラリのインストール

pip を使用して DuckDB の Python バインディングをインストールします。

```bash
# .venv 環境が有効化されていることを確認
pip install duckdb
```

これにより、プロジェクトの依存関係に DuckDB が追加されます (`requirements.txt` に記載されていることを確認してください)。

## 2. VSS 拡張のインストール (DuckDB 内から)

DuckDB のセッション内から SQL コマンドを実行して VSS 拡張をインストールし、ロードします。

```python
import duckdb

# DuckDB に接続 (インメモリまたはファイル)
con = duckdb.connect(database=':memory:', read_only=False)

# VSS 拡張のインストール
# 初回実行時のみ必要。データベースファイルに永続化する場合はファイルを開いて実行。
try:
    con.execute("INSTALL vss;")
except Exception as e:
    print(f"Failed to install VSS (might already be installed): {e}")

# VSS 拡張のロード (セッションごとに必要)
try:
    con.execute("LOAD vss;")
    print("VSS extension loaded successfully.")
except Exception as e:
    print(f"Failed to load VSS: {e}")

# これで VSS 拡張の機能が利用可能になります

# 接続を閉じる
con.close()
```

**注意点:**

*   `INSTALL vss;` は、指定した DuckDB 環境（またはデータベースファイル）に対して初回のみ実行が必要です。一度インストールされれば、次回以降は `LOAD vss;` のみで拡張機能を有効化できます。
*   インメモリデータベース (`:memory:`) を使用する場合、接続を閉じるたびに拡張機能も消えるため、毎回 `INSTALL` と `LOAD` が必要になる可能性があります（環境による）。永続的なデータベースファイルを使用する場合は、ファイルに拡張機能が保存されます。
