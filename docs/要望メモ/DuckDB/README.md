# DuckDB と VSS 拡張について

## DuckDB とは

DuckDB は、**OLAP (Online Analytical Processing) 分析に特化したインプロセス（組み込み型）のリレーショナルデータベース管理システム (RDBMS)** です。「SQLite の OLAP 版」とも表現されます。

### 主な特徴

*   **高速な分析処理:** 列指向ストレージとベクトル化実行エンジンにより、分析クエリを高速に処理します。
*   **インプロセス:** アプリケーションに直接組み込んで使用でき、外部サーバープロセスを必要としません。
*   **インストール不要:** 多くの場合、単一のファイルまたはライブラリとして提供され、セットアップが容易です。
*   **SQL サポート:** 標準 SQL に準拠しており、豊富な分析関数を提供します。
*   **多様なデータ形式の直接クエリ:** Parquet, CSV, JSON などのファイルを直接 SQL でクエリできます。圧縮ファイルも扱えます。
*   **Python との親和性:** Pandas DataFrame などとの連携が容易です。
*   **拡張性:** 拡張機能により、地理空間データ処理 (Spatial)、全文検索 (FTS)、ベクトル検索 (VSS) などの機能を追加できます。
*   **OSS:** MIT ライセンスで公開されています。

参考: [DuckDB 公式サイト](https://duckdb.org/)

## VSS (Vector Similarity Search) 拡張

DuckDB VSS 拡張は、DuckDB にベクトル類似性検索機能を追加します。

### 概要

*   高次元ベクトルデータに対して、類似度に基づいた検索 (最近傍探索) を行うための拡張機能です。
*   RAG (Retrieval-Augmented Generation) システムにおけるベクトルストアとして利用するなど、AI/ML アプリケーションでの活用が期待されます。

### 主な機能

*   **近似最近傍探索 (ANN):** `usearch` ライブラリに基づく HNSW (Hierarchical Navigable Small World) アルゴリズムを利用し、大規模なベクトルデータセットに対して高速な類似性検索を実現します。
*   **SQL インターフェース:** SQL を使用してインデックスの作成や検索を実行できます。

参考:
*   [DuckDB VSS Extension Blog Post](https://duckdb.org/2024/05/03/vector-similarity-search-vss.html)
*   [GitHub: duckdb/duckdb-vss](https://github.com/duckdb/duckdb-vss)

## セットアップ方法 (Python の場合)

1.  **DuckDB ライブラリのインストール:**
    ```bash
    pip install duckdb
    ```
    (通常、これで Python バインディングがインストールされます)

2.  **VSS 拡張のインストール (DuckDB 内から):**
    Python スクリプトまたは DuckDB CLI から以下の SQL を実行します。
    ```sql
    INSTALL vss;
    LOAD vss;
    ```
    これにより、現在のセッションまたはデータベースファイルに VSS 拡張がインストール・ロードされます。

## 基本的な使い方 (Python 例)

```python
import duckdb
import numpy as np

# データベースに接続 (ファイルまたはインメモリ)
con = duckdb.connect(database=':memory:', read_only=False)

# VSS拡張のインストールとロード
con.execute("INSTALL vss;")
con.execute("LOAD vss;")

# サンプルデータの準備 (ベクトルデータ)
vector_dim = 128  # 例: ベクトルの次元数
num_vectors = 1000
vectors = np.random.rand(num_vectors, vector_dim).astype('float32')
ids = list(range(num_vectors))

# テーブルの作成とデータの挿入
con.execute(f"CREATE TABLE items (id INTEGER, embedding FLOAT[{vector_dim}])")
for i, vec in zip(ids, vectors):
    con.execute("INSERT INTO items VALUES (?, ?)", [i, vec])

# HNSW インデックスの作成
con.execute(f"""
CREATE INDEX hnsw_index ON items USING HNSW (embedding)
WITH (metric = 'l2sq', # 距離メトリック (l2sq, cosine, ip)
      M = 16,          # HNSW パラメータ
      ef_search = 64,  # HNSW パラメータ
      ef_construction = 128) # HNSW パラメータ
""")

# 類似性検索の実行
query_vector = np.random.rand(vector_dim).astype('float32')
k = 5 # 上位 k 件を取得

result = con.execute(
    f"SELECT id FROM items ORDER BY array_distance(embedding, ?) LIMIT ?",
    [query_vector, k]
).fetchall()

print(f"Query Vector に最も類似する {k} 件の ID: {result}")

# 接続を閉じる
con.close()
```

このドキュメントは、DuckDB と VSS 拡張の基本的な概要と使い方を示しています。詳細については公式ドキュメントを参照してください。
