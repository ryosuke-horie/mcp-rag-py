# Document Processor (`rag_core.document_processor`)

## 目的

ドキュメントの読み込み (loading) と分割 (splitting) を担当するモジュール群です。様々な形式のドキュメントを処理し、RAGシステムが扱いやすい形式に変換します。

## 現状

-   初期のファイル (`__init__.py`, `loader.py`, `splitter.py`) が作成されました。
-   具体的なローダーやスプリッターの実装はこれから行います。
-   LangChain のドキュメントローダーとテキストスプリッターを利用する予定です。

## 関連コンポーネント

-   `rag_core`: このパッケージの親パッケージ。
-   `rag_core.embedding`: 分割されたテキストチャンクを埋め込みベクトルに変換するために連携します。
-   `rag_core.vectordb`: 処理されたドキュメント情報をベクトルDBに保存するために連携します。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../../docs/ADR/001-RAG実装の技術選定.md) (LangChainの利用方針)
