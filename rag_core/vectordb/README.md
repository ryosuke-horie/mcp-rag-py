# Vector Database (`rag_core.vectordb`)

## 目的

埋め込みベクトルと関連メタデータの保存、および類似ベクトル検索を担当します。ベクトルデータベースとして DuckDB と VSS (Vector Similarity Search) 拡張機能を利用します。

## 現状

-   初期のファイル (`__init__.py`, `storage.py`) が作成されました。
-   DuckDB への接続、テーブル作成、ベクトルデータの挿入・検索処理の実装はこれから行います。

## 関連コンポーネント

-   `rag_core`: このパッケージの親パッケージ。
-   `rag_core.document_processor`: 処理されたドキュメントのメタデータを保存するために連携します。
-   `rag_core.embedding`: 生成された埋め込みベクトルを保存するために連携します。
-   `mcp_server`: ユーザーからのクエリに基づいて類似ベクトルを検索する際に利用されます。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../../docs/ADR/001-RAG実装の技術選定.md) (DuckDB+VSSの選定理由)
