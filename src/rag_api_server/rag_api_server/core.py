from pathlib import Path
from typing import Any

from langchain_core.documents import Document

from rag_core.document_processor.loader import load_documents
from rag_core.document_processor.splitter import split_documents
from rag_core.embedding.model import (
    embed_query,
    embed_texts,
    initialize_embedding_model,
)
from rag_core.vectordb.storage import DuckDBVectorStore

from .config import settings


class RAGCore:
    """RAGコアコンポーネントを統合し、APIサーバーから利用可能にするクラス"""

    def __init__(self):
        """
        RAGコアコンポーネントの初期化

        Args:
            ollama_base_url: OllamaサーバーのベースURL
            model_name: 使用する埋め込みモデルの名前
            db_path: DuckDBデータベースのパス
            table_name: ベクトルを保存するテーブル名
        """
        self.embeddings = initialize_embedding_model(
            ollama_base_url=settings.ollama_base_url,
            model_name=settings.embedding_model_name,
        )
        self.vector_store = DuckDBVectorStore(
            db_path=settings.db_path, table_name=settings.table_name
        )
        print("RAGCoreの初期化が完了しました。")

    async def process_directory(
        self, directory_path: str, glob_pattern: str = "**/*[.md|.txt]"
    ) -> dict[str, Any]:
        """
        ディレクトリ内のドキュメントを処理し、ベクトルDBに保存する

        Args:
            directory_path: 処理対象のディレクトリパス
            glob_pattern: ファイルのフィルタリングパターン

        Returns:
            処理結果を含む辞書
        """
        try:
            # ディレクトリパスの正規化
            dir_path = Path(directory_path).resolve()
            if not dir_path.is_dir():
                raise ValueError(f"無効なディレクトリパス: {directory_path}")

            # ドキュメントの読み込み
            print(f"ドキュメントを読み込み中: {dir_path}...")
            documents = load_documents(str(dir_path), glob_pattern=glob_pattern)
            if not documents:
                return {
                    "status": "no_documents",
                    "message": "指定されたディレクトリにドキュメントが見つかりません",
                }

            # ドキュメントの分割
            print("ドキュメントをチャンクに分割中...")
            chunks = split_documents(documents)
            if not chunks:
                return {
                    "status": "no_chunks",
                    "message": "ドキュメントからチャンクが生成されませんでした",
                }

            # テキストとメタデータの抽出
            texts = [chunk.page_content for chunk in chunks]

            # 埋め込みの生成
            print("埋め込みを生成中...")
            embeddings = embed_texts(texts, self.embeddings)

            # ベクトルDBへの保存
            print("ベクトルDBに保存中...")
            self.vector_store.add_embeddings(texts, embeddings)

            return {
                "status": "success",
                "processed_documents": len(documents),
                "processed_chunks": len(chunks),
                "message": "ドキュメントの処理が完了しました",
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"ドキュメント処理中にエラーが発生しました: {str(e)}",
            }

    async def query(
        self, query_text: str, k: int = 4, filter_criteria: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        クエリに対して類似ドキュメントを検索する

        Args:
            query_text: 検索クエリのテキスト
            k: 返却する類似ドキュメントの数
            filter_criteria: 検索結果をフィルタリングするための条件

        Returns:
            検索結果を含む辞書
        """
        try:
            # クエリの埋め込みを生成
            query_embedding = embed_query(query_text, self.embeddings)

            # ベクトルDBで類似検索
            # filter_criteriaパラメータは使用されていないため削除
            results = self.vector_store.similarity_search(query_embedding, k=k)

            # 返却結果の構造を修正
            # vectordb.storage.py の similarity_search メソッドはタプルのリストを返す
            # 例: [('doc1 text', 0.98), ('doc2 text', 0.95)]
            return {
                "status": "success",
                "results": [
                    {
                        "text": text,
                        "similarity": similarity,
                    }
                    for text, similarity in results
                ],
                "message": "検索が完了しました",
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"検索中にエラーが発生しました: {str(e)}",
            }

    async def add_single_content(
        self, content: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        単一のテキストコンテンツを処理し、チャンク化してベクトルDBに保存する

        Args:
            content: 登録するテキストコンテンツ
            metadata: コンテンツに関連するメタデータ (オプション)

        Returns:
            処理結果を含む辞書
        """
        try:
            # コンテンツをDocumentオブジェクトに変換
            doc_metadata = metadata if metadata is not None else {}
            document = Document(page_content=content, metadata=doc_metadata)

            # ドキュメントの分割
            print("コンテンツをチャンクに分割中...")
            chunks = split_documents([document])
            if not chunks:
                return {
                    "status": "no_chunks",
                    "message": "コンテンツからチャンクが生成されませんでした",
                }

            # テキストとメタデータの抽出
            texts = [chunk.page_content for chunk in chunks]

            # 埋め込みの生成
            print("埋め込みを生成中...")
            embeddings = embed_texts(texts, self.embeddings)

            # ベクトルDBへの保存
            print("ベクトルDBに保存中...")
            self.vector_store.add_embeddings(texts, embeddings)

            return {
                "status": "success",
                "processed_chunks": len(chunks),
                "message": "コンテンツの処理が完了しました",
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"コンテンツ処理中にエラーが発生しました: {str(e)}",
            }

    def close(self):
        """リソースの解放"""
        if hasattr(self, "vector_store"):
            self.vector_store.close()
