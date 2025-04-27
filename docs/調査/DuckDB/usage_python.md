# DuckDB + VSS 拡張 Python での使い方と注意点

## 基本的な使い方 (Python 例)

以下は、DuckDB と VSS 拡張を使用して、ベクトルデータの保存、HNSW インデックスの作成、類似性検索を行う基本的な Python コード例です。

```python
import duckdb
import numpy as np

# データベースに接続 (ファイルまたはインメモリ)
con = duckdb.connect(database=':memory:', read_only=False)

# VSS拡張のインストールとロード (setup.md 参照)
try:
    con.execute("INSTALL vss;")
except Exception: pass # Ignore if already installed
try:
    con.execute("LOAD vss;")
except Exception as e:
    print(f"Failed to load VSS: {e}")
    exit()

# --- データ準備 ---
vector_dim = 128  # ベクトルの次元数 (実際のモデルに合わせる)
num_vectors = 1000
vectors = np.random.rand(num_vectors, vector_dim).astype('float32') # 型は float32
ids = list(range(num_vectors))

# --- テーブル作成とデータ挿入 ---
# HNSW インデックスのため、カラム型は FLOAT[N] (固定長) にする
con.execute(f"CREATE OR REPLACE TABLE items (id INTEGER, embedding FLOAT[{vector_dim}])")

# executemany で効率的に挿入 (NumPy 配列はリストに変換)
data_to_insert = list(zip(ids, vectors.tolist()))
con.executemany("INSERT INTO items VALUES (?, ?)", data_to_insert)
print(f"Inserted {len(data_to_insert)} items.")

# --- HNSW インデックス作成 ---
# metric: l2sq (ユークリッド距離の二乗), cosine (コサイン類似度), ip (内積)
# パラメータ (M, ef_search, ef_construction) はデータや要件に応じて調整
con.execute(f"""
CREATE INDEX hnsw_index ON items USING HNSW (embedding)
WITH (metric = 'l2sq', M = 16, ef_search = 64, ef_construction = 128)
""")
print("HNSW index created.")

# --- 類似性検索 ---
query_vector = np.random.rand(vector_dim).astype('float32') # 検索ベクトルも float32
k = 5 # 上位 k 件

# HNSW インデックス検索には <-> 演算子を使用
# パラメータを ?::FLOAT[] でキャストする
sql = f"SELECT id, embedding <-> ?::FLOAT[] AS distance FROM items ORDER BY distance LIMIT ?"
result = con.execute(sql, [query_vector, k]).fetchall()

print(f"\nQuery Vector に最も類似する {k} 件 (ID, Distance):")
for row in result:
    print(f"  ID: {row[0]}, Distance: {row[1]:.4f}")

# 接続を閉じる
con.close()
```

## Python での利用における注意点 (HNSW + 類似性検索)

Python から DuckDB VSS 拡張を利用して HNSW インデックスを作成し、類似性検索を行う際には、特にデータ型に関して注意が必要です。

1.  **HNSW インデックスのカラム型:**
    *   HNSW インデックスを作成するカラムは、**固定長の浮動小数点配列 (`FLOAT[N]`)** である必要があります。可変長 (`FLOAT[]`) ではインデックスを作成できません。
    *   例: `CREATE TABLE items (id INTEGER, embedding FLOAT[128])`

2.  **類似性検索の方法:**
    *   HNSW インデックスを利用した効率的な類似性検索には、`array_distance` 関数ではなく、専用の距離演算子 **`<->`** を使用することが推奨されます。この演算子はインデックスを活用します。
    *   例: `SELECT id FROM items ORDER BY embedding <-> ?`

3.  **パラメータの型:**
    *   Python から `float32` 型の NumPy 配列をパラメータ (`?`) として渡す場合、DuckDB が内部的に `DOUBLE[]` として解釈し、`FLOAT[N]` カラムとの間で型不一致エラーが発生することがあります。
    *   これを回避するには、SQL クエリ内でパラメータを明示的に **`FLOAT[]` にキャスト (`?::FLOAT[]`)** します。
    *   例: `sql = "SELECT id FROM items ORDER BY embedding <-> ?::FLOAT[] LIMIT ?"`
          `result = con.execute(sql, [query_vector, k]).fetchall()`

## 試行錯誤の過程

セットアップ確認中に、類似性検索で以下のような問題が発生しました。

*   **問題:** `array_distance` 関数とパラメータ (`?`) を使用した際、`FLOAT[N]` カラムと `DOUBLE[]` (Python から渡されたパラメータ) 間の型不一致エラー (`Binder Error`) が発生。
*   **試行1:** カラムやパラメータを `DOUBLE[]` または `FLOAT[]` にキャスト → `array_distance` 関数や HNSW インデックスとの互換性問題で失敗。
*   **試行2:** カラム型を `FLOAT[]` (可変長) に変更 → HNSW インデックスが `FLOAT[N]` (固定長) を要求するため失敗。
*   **解決策:**
    1.  類似性検索に HNSW インデックス用の **`<->` 演算子**を使用。
    2.  テーブルカラムは HNSW の要件通り **`FLOAT[N]` (固定長)** を維持。
    3.  SQL クエリ内で検索ベクトルパラメータを **`?::FLOAT[]`** と明示的にキャスト。

これにより、Python の `float32` NumPy 配列を正しく渡し、HNSW インデックスを利用した類似性検索を実行できました。
