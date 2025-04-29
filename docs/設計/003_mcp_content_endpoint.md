# API設計: MCPからのコンテンツ登録エンドポイント

## 1. 背景

既存の `/documents/` エンドポイントはファイルシステム上のドキュメントを処理対象としており、MCP (Model Context Protocol) など外部ソースが動的に取得したテキストコンテンツを直接ベクトルDBに登録する用途には適していない。
そのため、MCPからの調査結果などを直接RAGシステムに登録するための新しいAPIエンドポイントを設計する。

## 2. エンドポイント仕様

-   **目的:** MCPなど外部ソースから提供されたテキストコンテンツを直接ベクトルDBに登録する。
-   **パス:** `/contents/`
-   **HTTPメソッド:** `POST`
-   **リクエストボディ (JSON):**
    ```json
    {
      "content": "登録したいテキストコンテンツ...", // string, 必須
      "metadata": { // object, オプション (初期実装では省略可)
        "source_description": "取得元などの説明", // 例: "Brave Search result for 'XYZ'"
        "source_url": "https://example.com/source", // 例: 検索結果のURL
        "timestamp": "2025-04-29T15:10:00Z" // 例: 取得タイムスタンプ
      }
    }
    ```
-   **レスポンスボディ (成功時, `200 OK`):**
    ```json
    {
      "status": "success",
      "message": "Content processed and added successfully.",
      "processed_chunks": 5 // 処理されたチャンク数
      // "content_ids": [101, 102, 103, 104, 105] // オプション: 登録されたチャンクのIDリスト
    }
    ```
-   **レスポンスボディ (バリデーションエラー, `422 Unprocessable Entity`):** FastAPI標準のエラーレスポンス。
-   **レスポンスボディ (処理エラー, `500 Internal Server Error`):**
    ```json
    {
      "detail": "Error processing content: <エラー詳細>"
    }
    ```

## 3. 処理フロー

1.  FastAPI (`main.py`) で `POST /contents/` リクエストを受け付ける。
2.  リクエストボディから `content` （およびオプションで `metadata`）を取得する。
3.  `RAGCore` (`core.py`) に新設するメソッド `add_single_content(content: str, metadata: Optional[dict] = None)` を呼び出す。
4.  `add_single_content` メソッド内で:
    a.  受け取った `content` 文字列を `langchain_core.documents.Document` オブジェクトに変換する。（`metadata` もここで含める）
    b.  `rag_core.document_processor.splitter.split_documents` を使用して `Document` をチャンクに分割する。
    c.  分割された各チャンクからテキスト (`texts`) とメタデータ (`metadatas`) を抽出する。
    d.  `rag_core.embedding.model.embed_texts` を使用して、各チャンクテキストの埋め込みベクトル (`embeddings`) を生成する。
    e.  `DuckDBVectorStore` (`storage.py`) の `add_embeddings` メソッドを呼び出して、チャンクテキスト、埋め込みベクトル、（可能であれば）メタデータをDBに保存する。
5.  処理結果（成功したチャンク数など）を含む成功レスポンス、またはエラーレスポンスを返す。

## 4. 主なコード変更箇所

-   **`src/rag_api_server/rag_api_server/main.py`**:
    -   新しいPydanticモデル `ContentRequest`, `ContentResponse` を定義する。
    -   `/contents/` パスオペレーションを追加し、`RAGCore.add_single_content` を呼び出すように実装する。
-   **`src/rag_api_server/rag_api_server/core.py`**:
    -   `RAGCore` クラスに `add_single_content` メソッドを追加する。このメソッドは上記「3. 処理フロー」のステップ 4a〜4e を実装する。
    -   `split_documents` を文字列リストではなく `Document` オブジェクトのリストを受け付けるように調整するか、`content` を `Document` に変換する処理を追加する。
-   **`src/rag_core/rag_core/vectordb/storage.py`** (検討・変更可能性あり):
    -   `add_embeddings` メソッドがメタデータも受け取り、保存できるようにテーブルスキーマと挿入ロジックを更新する。（初期実装では省略し、テキストのみ保存も可）
    -   （オプション）`add_embeddings` が挿入したレコードのIDリストを返すように変更する。

## 5. 検討事項

-   **メタデータの扱い:** 初期実装では `metadata` を省略し、テキストコンテンツのみを登録するシンプルな実装から始めることも可能。必要に応じて後からメタデータ保存機能を追加する。
-   **IDの返却:** 登録されたチャンクのIDをレスポンスで返す必要があるか検討する。必須でなければ省略可能。
-   **エラーハンドリング:** 各ステップでのエラー（埋め込み生成失敗、DB保存失敗など）を適切にハンドリングし、クライアントに分かりやすいエラーメッセージを返す。
-   **`split_documents` 関数の入力:** 現在の実装が `List[Document]` を期待しているため、`add_single_content` 内で受け取った `content` 文字列を `Document` オブジェクトに変換する必要がある。
