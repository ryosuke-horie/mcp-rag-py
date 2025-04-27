# Vector Database (`rag_core.vectordb`)

## 目的

埋め込みベクトルと関連メタデータの保存、および類似ベクトル検索を担当します。ベクトルデータベースとして DuckDB と VSS (Vector Similarity Search) 拡張機能を利用します。

## 実装の詳細

### `DuckDBVectorStore` クラス

`storage.py` に実装された `DuckDBVectorStore` クラスは以下の機能を提供します：

1. **初期化とセットアップ**
   - DuckDB データベースへの接続
   - VSS拡張機能のインストールとロード
   - テーブルの自動作成（存在しない場合）

2. **テーブル構造**
   ```sql
   CREATE TABLE IF NOT EXISTS {table_name} (
       id INTEGER PRIMARY KEY,  -- 自動採番ID
       text VARCHAR,           -- テキストデータ
       embedding FLOAT[1024]   -- 埋め込みベクトル（bge-m3用に1024次元）
   );
   ```

3. **主要メソッド**
   - `add_embeddings(texts: List[str], embeddings: List[np.ndarray])`: 
     - テキストと埋め込みベクトルを一括で追加
     - IDは自動的に連番が付与
   - `similarity_search(query_embedding: np.ndarray, k: int = 5)`:
     - コサイン類似度による類似ベクトル検索
     - `array_cosine_similarity` 関数を使用
     - 類似度スコアの高い順にk件を返却

## 動作確認

基本的な機能は `storage.py` を直接実行することでテストできます：

```bash
# プロジェクトルートディレクトリから実行
python3 rag_core/vectordb/storage.py
```

テストプログラムの処理フロー：

1. テスト用DBファイル `test_vector_store.db` を作成（既存の場合は削除して再作成）
2. `test_embeddings` テーブルを作成
3. サンプルテキスト3件とそのランダムな埋め込みベクトルを登録
4. ランダムなクエリベクトルで類似検索を実行（上位2件）
5. DB接続を終了

**注意:** 
- 実行後、`test_vector_store.db` ファイルがカレントディレクトリに作成されます
- このファイルは手動で削除するか、次回テスト実行時に自動的に削除されます

## 関連コンポーネント

-   `rag_core`: このパッケージの親パッケージ。
-   `rag_core.document_processor`: 処理されたドキュメントのメタデータを保存するために連携します。
-   `rag_core.embedding`: 生成された埋め込みベクトルを保存するために連携します。
-   `mcp_server`: ユーザーからのクエリに基づいて類似ベクトルを検索する際に利用されます。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../../docs/ADR/001-RAG実装の技術選定.md) (DuckDB+VSSの選定理由)
