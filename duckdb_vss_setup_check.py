import duckdb
import numpy as np
import os

# .venv 内の Python を使うことを想定

print("--- DuckDB VSS Extension Setup Check ---")

try:
    # インメモリデータベースに接続
    con = duckdb.connect(database=':memory:', read_only=False)
    print("[1/6] Connected to in-memory DuckDB.")

    # VSS拡張のインストールとロード
    print("[2/6] Installing VSS extension...")
    con.execute("INSTALL vss;")
    print("[3/6] Loading VSS extension...")
    con.execute("LOAD vss;")
    print("   VSS extension installed and loaded successfully.")

    # サンプルデータの準備
    vector_dim = 8  # 次元数を小さくしてテスト
    num_vectors = 100
    vectors = np.random.rand(num_vectors, vector_dim).astype('float32')
    ids = list(range(num_vectors))
    print(f"[4/6] Prepared sample data ({num_vectors} vectors, dim={vector_dim}).")

    # テーブル作成とデータ挿入
    con.execute(f"CREATE TABLE items (id INTEGER, embedding FLOAT[{vector_dim}])") # Revert back to FLOAT[vector_dim] for HNSW index
    # executemany を使用して効率化
    data_to_insert = list(zip(ids, vectors.tolist())) # numpy 配列をリストに変換
    con.executemany("INSERT INTO items VALUES (?, ?)", data_to_insert)
    print("   Created table 'items' and inserted data.")

    # HNSW インデックス作成
    print("[5/6] Creating HNSW index...")
    con.execute(f"""
    CREATE INDEX hnsw_index ON items USING HNSW (embedding)
    WITH (metric = 'l2sq', M = 8, ef_search = 32, ef_construction = 64)
    """)
    print("   HNSW index created successfully.")

    # 類似性検索の実行
    query_vector = np.random.rand(vector_dim).astype('float32')
    k = 3
    print(f"[6/6] Performing similarity search for top {k} results...")
    # Construct the vector literal string like '[1.0, 2.0, ...]'
    # Use the <-> distance operator designed for HNSW index search
    # Cast the parameter to FLOAT[] to match the expected type
    sql = f"SELECT id FROM items ORDER BY embedding <-> ?::FLOAT[] LIMIT ?"
    result = con.execute(sql, [query_vector, k]).fetchall()

    print(f"   Similarity search successful. Found IDs: {result}")
    print("\n--- Check Complete: DuckDB and VSS extension seem to be working correctly. ---")

except Exception as e:
    print(f"\n--- ERROR during setup check: {e} ---")

finally:
    if 'con' in locals() and con:
        con.close()
        print("   Database connection closed.")
