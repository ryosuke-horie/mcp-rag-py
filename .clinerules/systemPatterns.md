# System Patterns

## システムアーキテクチャ

- (ここにシステム全体の構成図や説明を記述)
- 例:
    ```mermaid
    graph TD
        A[User Interface] --> B(MCP Server);
        B --> C{RAG System};
        C --> D[Embedding Model];
        C --> E[Vector DB (DuckDB+VSS)];
        E --> F[Document Store];
    ```

## 主要な技術的決定

- (ここに行った主要な技術選択とその理由を記述)
- 例: ベクトルDBとしてDuckDB+VSSを選択（理由: ローカルでの容易なセットアップ、SQLライクな操作性）

## デザインパターン

- (ここで採用しているデザインパターンを記述)
- 例: Retrieval-Augmented Generation (RAG) パターン

## コンポーネントの関係

-   **`rag_core.document_processor`**:
    -   ドキュメントの読み込みには LangChain の `DirectoryLoader` および `TextLoader` を利用し、`.txt` と `.md` ファイルを処理する。
    -   テキストの分割には LangChain の `RecursiveCharacterTextSplitter` を利用し、チャンクサイズ 1000、オーバーラップ 200 で分割する。
    -   読み込み・分割されたドキュメント（チャンク）は、後続の `rag_core.embedding` コンポーネントに渡される。
- (他のコンポーネント間の連携方法やインターフェースを記述)

## クリティカルな実装パス

- (ここにシステムの中心となる処理フローや特に注意が必要な実装箇所を記述)
