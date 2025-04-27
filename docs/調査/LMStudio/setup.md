# LM Studio で pfnet/plamo-embedding-1b モデルを利用する手順

LM Studio を使用して、Hugging Face で公開されている `pfnet/plamo-embedding-1b` 埋め込みモデルをダウンロードし、ローカル API サーバー経由で利用可能にするための手順を以下に示します。

## 1. LM Studio の起動

まず、インストール済みの LM Studio アプリケーションを起動します。

## 2. モデルの検索

LM Studio のメイン画面（または「Discover」や「Search」タブ）にある検索バーに `pfnet/plamo-embedding-1b` と入力してモデルを検索します。

![LM Studio Search](https://lmstudio.ai/images/docs/search.png) <!-- 画像はLM Studio公式ドキュメントより引用 -->

## 3. モデルのダウンロード

検索結果に `pfnet/plamo-embedding-1b` が表示されたら、それを選択します。
モデルの詳細画面で、利用可能なファイル形式（通常は GGUF 形式が推奨されます）を確認し、適切なファイルをダウンロードします。

**注意点:**
-   `pfnet/plamo-embedding-1b` モデルページ ([https://huggingface.co/pfnet/plamo-embedding-1b](https://huggingface.co/pfnet/plamo-embedding-1b)) で GGUF 形式が提供されているか事前に確認しておくとスムーズです。
-   LM Studio が直接 GGUF 形式を提供していない場合、他の互換性のある埋め込みモデルを探すか、モデル形式の変換が必要になる可能性があります。まずは LM Studio 内での検索とダウンロードを試してください。

## 4. ローカルサーバーのセットアップと起動

モデルのダウンロードが完了したら、LM Studio の「Local Server」タブ（またはそれに類するセクション）に移動します。

1.  **モデルの選択:** 画面上部のモデル選択ドロップダウンから、ダウンロードした `pfnet/plamo-embedding-1b` モデルを選択します。
2.  **サーバー設定の確認:**
    -   LM Studio は通常、OpenAI 互換の API エンドポイントを提供します。埋め込み用途の場合、`/v1/embeddings` エンドポイントが利用可能になるはずです。
    -   サーバー設定（ポート番号、コンテキスト長など）を確認し、必要に応じて調整します。特に「Embeddings」に関連する設定項目がないか確認してください。
    -   ハードウェアアクセラレーション（GPU オフロードなど）の設定も確認し、環境に合わせて最適化します。
3.  **サーバーの起動:** 設定が完了したら、「Start Server」ボタンをクリックしてローカル API サーバーを起動します。

![LM Studio Local Server](https://lmstudio.ai/images/docs/local-server.png) <!-- 画像はLM Studio公式ドキュメントより引用 -->

## 5. API エンドポイントの確認

サーバーが正常に起動すると、LM Studio は利用可能な API エンドポイントのベース URL（例: `http://localhost:1234/v1`）を表示します。

埋め込みを取得するためのエンドポイントは、通常このベース URL に `/embeddings` を追加した `http://localhost:1234/v1/embeddings` となります。

このエンドポイントを、RAG システムの `rag_core/embedding/model.py` など、埋め込みモデルを利用するコンポーネントから呼び出すように設定します。

## 次のステップ

LM Studio で埋め込みモデルサーバーが起動できたら、`rag_core` の実装を進め、このローカルエンドポイントを利用してドキュメントのベクトル化を行う部分を実装します。
