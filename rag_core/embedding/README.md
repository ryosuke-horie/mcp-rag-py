# Embedding (`rag_core.embedding`)

## 目的

テキストチャンクを埋め込みベクトル (embedding vector) に変換する処理を担当します。選定された埋め込みモデル (`pfnet/plamo-embedding-1b`) のロードと利用を行います。

## 現状

-   初期のファイル (`__init__.py`, `model.py`) が作成されました。
-   埋め込みモデルのロードとベクトル化処理の実装はこれから行います。
-   `sentence-transformers` ライブラリを利用してモデルを扱う予定です。

## 関連コンポーネント

-   `rag_core`: このパッケージの親パッケージ。
-   `rag_core.document_processor`: このモジュールで分割されたテキストチャンクを受け取り、ベクトル化します。
-   `rag_core.vectordb`: 生成された埋め込みベクトルをベクトルDBに保存するために連携します。
-   `mcp_server`: ユーザーからのクエリをベクトル化する際にも利用されます。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../../docs/ADR/001-RAG実装の技術選定.md) (埋め込みモデルの選定理由)
