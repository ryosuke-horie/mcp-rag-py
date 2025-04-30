import os

import duckdb
import numpy as np


class DuckDBVectorStore:
    """
    VSS拡張機能を使用したDuckDBベースのベクトルストア実装
    """

    def __init__(
        self, db_path: str = "vector_store.db", table_name: str = "embeddings"
    ):
        """
        DuckDBVectorStoreを初期化します。

        Args:
            db_path (str): DuckDBデータベースファイルのパス。
            table_name (str): 埋め込みを格納するテーブルの名前。
        """
        self.db_path = db_path
        self.table_name = table_name
        self.embedding_dim = 1024  # bge-m3の次元

        try:
            self.conn = duckdb.connect(database=self.db_path, read_only=False)
            # VSS拡張機能をインストールしてロード（まだ行われていない場合）
            self.conn.execute("INSTALL vss;")
            self.conn.execute("LOAD vss;")
            # テーブルが存在しない場合は作成
            self._create_table()
        except Exception as e:
            print(f"DuckDBVectorStoreの初期化エラー: {e}")
            raise

    def _create_table(self):
        """埋め込みテーブルが存在しない場合に作成します。"""
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            text VARCHAR,
            embedding FLOAT[{self.embedding_dim}]
        );
        """
        try:
            self.conn.execute(create_table_sql)
        except Exception as e:
            print(f"テーブル作成エラー: {e}")
            raise

    def add_embeddings(self, texts: list[str], embeddings: list[list[float]]):
        """
        テキストチャンクとそれに対応する埋め込みをストアに追加します。

        Args:
            texts (List[str]): テキストチャンクのリスト。
            embeddings (List[List[float]]): 対応する埋め込み（浮動小数点数のリスト）のリスト。
        """
        if len(texts) != len(embeddings):
            raise ValueError("テキストと埋め込みの数が一致しません。")
        if not embeddings:
            print("追加する埋め込みがありません。")
            return

        # 次に利用可能なIDを取得
        try:
            max_id = self.conn.execute(
                f"SELECT COALESCE(MAX(id), 0) FROM {self.table_name}"
            ).fetchone()[0]
        except Exception:
            max_id = 0

        # 安全な挿入のためのパラメータ化クエリ
        insert_sql = (
            f"INSERT INTO {self.table_name} (id, text, embedding) VALUES (?, ?, ?)"
        )

        try:
            self.conn.begin()  # トランザクション開始
            # 手動で管理されたIDを使用して行ごとにデータを挿入
            for i, (text, embedding) in enumerate(
                zip(texts, embeddings, strict=False), start=1
            ):
                self.conn.execute(insert_sql, [max_id + i, text, embedding])
            self.conn.commit()  # すべての挿入が成功した場合に変更をコミット
            print(f"{len(texts)}個の埋め込みを正常に追加しました。")
        except Exception as e:
            print(f"埋め込み追加エラー: {e}")
            self.conn.rollback()  # エラー時にロールバック
            raise
        # finallyブロックは不要（接続のクローズは`close`メソッドで処理）

    def similarity_search(
        self, query_embedding: list[float], k: int = 5
    ) -> list[tuple[str, float]]:
        """
        コサイン類似度を使用して類似検索を実行します。

        Args:
            query_embedding (List[float]): クエリの埋め込み（浮動小数点数のリスト）。
            k (int): 取得する最近傍の数。

        Returns:
            List[Tuple[str, float]]: (テキスト, 類似度スコア)のタプルのリスト。
        """
        # オプション: 必要に応じてリストの長さチェックを追加
        # if len(query_embedding) != self.embedding_dim:
        #     raise ValueError(f"クエリ埋め込みの次元が一致しません。期待値: {self.embedding_dim}, 実際: {len(query_embedding)}")

        # コサイン類似度にarray_distanceを使用（1 - コサイン距離）
        # 注: VSSは新しいバージョンでコサイン類似度にlist_similarityを直接使用しますが、
        # array_distanceは一般的に利用可能です。コサイン類似度 = 1 - コサイン距離
        search_sql = f"""
        SELECT text, array_cosine_similarity(embedding, ?::FLOAT[1024]) AS similarity
        FROM {self.table_name}
        ORDER BY similarity DESC
        LIMIT ?;
        """
        try:
            results = self.conn.execute(search_sql, [query_embedding, k]).fetchall()
            # 結果を目的の形式（テキスト、スコア）に変換
            # fetchallはタプルのリストを返します。例: [('doc1 text', 0.98), ('doc2 text', 0.95)]
            return results
        except Exception as e:
            print(f"類似検索中のエラー: {e}")
            return []

    def close(self):
        """データベース接続を閉じます。"""
        if self.conn:
            self.conn.close()
            print("DuckDB接続を閉じました。")


# 使用例（オプション - テスト用）
if __name__ == "__main__":
    db_file = "test_vector_store.db"
    # 古いDBファイルが存在する場合は削除してクリーンな状態を確保
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"既存のデータベースファイルを削除しました: {db_file}")

    # 例: ストアを初期化
    store = DuckDBVectorStore(db_path=db_file, table_name="test_embeddings")

    # 例: 埋め込みを追加
    texts_to_add = [
        "これは最初のドキュメントです。",
        "このドキュメントはアヒルについてです。",
        "3番目の例示ドキュメントです。",
    ]
    # ダミーの埋め込み（実際のモデルからの埋め込みに置き換えてください）
    dummy_embeddings = [np.random.rand(1024).astype(np.float32) for _ in texts_to_add]
    store.add_embeddings(texts_to_add, dummy_embeddings)

    # 例: 類似検索
    query_vec = np.random.rand(1024).astype(np.float32)
    similar_docs = store.similarity_search(query_vec, k=2)
    print("\n類似検索結果:")
    for text, score in similar_docs:
        print(f"スコア: {score:.4f} - テキスト: {text}")

    # クリーンアップ
    store.close()
    # os.remove(db_file) # コメントアウトを維持、削除は開始時に行われます
    # print("テストデータベースファイルを削除しました。")
