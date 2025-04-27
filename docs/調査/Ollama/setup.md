# Ollama で埋め込みモデルを利用する手順

Ollama を使用して、ローカル環境で埋め込みモデルをダウンロードし、API 経由で利用可能にするための手順を以下に示します。

## 1. Ollama のインストール

Ollama がまだインストールされていない場合は、公式サイト ([https://ollama.com/](https://ollama.com/)) からダウンロードしてインストールします。

## 2. モデルのダウンロード (Pull)

利用したい埋め込みモデルを Ollama にダウンロードします。ターミナルを開き、以下のコマンドを実行します。

-   **利用可能なモデルの検索 (オプション):**
    ```bash
    ollama search <検索キーワード>
    # 例: ollama search embed
    ```
    [https://ollama.com/library?q=&f=embedding](https://ollama.com/library?q=&f=embedding) で埋め込みモデルの一覧を確認することもできます。

-   **モデルのダウンロード:**
    利用するモデル名を指定して `pull` コマンドを実行します。多言語対応の `bge-m3` モデルを使用します。
    ```bash
    ollama pull bge-m3
    ```
    *他の候補例: `nomic-embed-text`, `mxbai-embed-large`, `all-minilm` など*

## 3. Ollama サーバーの起動確認

Ollama は通常、インストール後や `pull` コマンド実行後にバックグラウンドでサーバープロセスが自動的に起動します。

-   **起動確認 (オプション):**
    別のターミナルを開き、以下の `curl` コマンドでサーバーが応答するか確認できます。
    ```bash
    curl http://localhost:11434/
    ```
    "Ollama is running" と表示されれば正常に起動しています。

-   **手動起動 (必要な場合):**
    もしサーバーが起動していない場合は、アプリケーションフォルダから Ollama を起動するか、ターミナルで以下のコマンドを実行します。
    ```bash
    ollama serve
    ```

## 4. 埋め込み API エンドポイントのテスト

Ollama サーバーが起動している状態で、`/api/embeddings` エンドポイントを使って埋め込みベクトルを生成できるかテストします。

-   ターミナルで以下の `curl` コマンドを実行します（`model` の値はダウンロードした `bge-m3` に合わせてください）。
    ```bash
    curl http://localhost:11434/api/embeddings -d '{
      "model": "bge-m3",
      "prompt": "これは埋め込み生成のテストです。"
    }'
    ```

-   **成功時の応答例:**
    ```json
    {
      "embedding": [
        0.5123, -0.1234, ..., 0.9876
      ]
    }
    ```
    上記のように `embedding` キーを持つ JSON が返却されれば、API が正常に機能しています。

## 5. RAG システムでの利用

この API エンドポイント (`http://localhost:11434/api/embeddings`) とモデル名 (`bge-m3`) を、RAG システムの埋め込み生成コンポーネント (`rag_core/embedding/model.py` など) で設定し、利用します。

LangChain を使用する場合は `OllamaEmbeddings` クラスが利用できます。

```python
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="bge-m3")
# embeddings = OllamaEmbeddings(model="bge-m3", base_url="http://localhost:11434") # デフォルトURL以外の場合

text = "テストテキスト"
query_result = embeddings.embed_query(text)
# doc_result = embeddings.embed_documents([text1, text2])
```

これで、ローカルの Ollama サーバーを使ってテキストの埋め込みベクトルを生成する準備が整いました。
