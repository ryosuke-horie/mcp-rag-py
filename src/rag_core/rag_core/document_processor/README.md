# Document Processor (`rag_core.document_processor`)

## 目的

ドキュメントの読み込み (loading) と分割 (splitting) を担当するモジュール群です。様々な形式のドキュメントを処理し、RAGシステムが扱いやすい形式に変換します。

## 現状

-   **`loader.py`**: LangChain の `DirectoryLoader` と `TextLoader` を使用して、指定ディレクトリ内の `.txt` および `.md` ファイルを読み込む `load_documents` 関数を実装済み。
-   **`splitter.py`**: LangChain の `RecursiveCharacterTextSplitter` を使用して、ドキュメントを指定されたチャンクサイズ (デフォルト 1000) とオーバーラップ (デフォルト 200) で分割する `split_documents` 関数を実装済み。
-   **`__init__.py`**: 上記関数を外部からインポート可能に設定済み。

## 関連コンポーネント

-   `rag_core`: このパッケージの親パッケージ。
-   `rag_core.embedding`: 分割されたテキストチャンクを埋め込みベクトルに変換するために連携します。
-   `rag_core.vectordb`: 処理されたドキュメント情報をベクトルDBに保存するために連携します。

## 関連ドキュメント

-   [ADR 001: RAG実装の技術選定](../../../docs/ADR/001-RAG実装の技術選定.md) (LangChainの利用方針)

## 動作確認

各モジュールには、基本的な動作を確認するためのテストコードが含まれています (`if __name__ == '__main__':` ブロック内)。
プロジェクトのルートディレクトリから以下のコマンドを実行することで、それぞれのテストを実行できます。

### ローダー (`loader.py`) のテスト

```bash
python3 rag_core/document_processor/loader.py
```

このテストは、一時的なディレクトリとファイルを作成し、`.txt` および `.md` ファイルが正しく読み込まれるかを確認します。テスト完了後、作成された一時ファイルは自動的に削除されます。

### スプリッター (`splitter.py`) のテスト

```bash
python3 rag_core/document_processor/splitter.py
```

このテストは、ダミーの長文ドキュメントを作成し、デフォルト設定およびカスタム設定でテキストがチャンクに分割されることを確認します。
