from pathlib import Path
from typing import Any

from langchain_core.documents import Document  # Documentを追加

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
        print("RAGCore initialized successfully.")

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
                raise ValueError(f"Invalid directory path: {directory_path}")

            # ドキュメントの読み込み
            print(f"Loading documents from {dir_path}...")
            documents = load_documents(str(dir_path), glob_pattern=glob_pattern)
            if not documents:
                return {
                    "status": "no_documents",
                    "message": "No documents found in the specified directory",
                }

            # ドキュメントの分割
            print("Splitting documents into chunks...")
            chunks = split_documents(documents)
            if not chunks:
                return {
                    "status": "no_chunks",
                    "message": "No chunks created from the documents",
                }

            # テキストとメタデータの抽出
            texts = [chunk.page_content for chunk in chunks]

            # 埋め込みの生成
            print("Generating embeddings...")
            embeddings = embed_texts(texts, self.embeddings)

            # ベクトルDBへの保存
            print("Storing embeddings in the vector database...")
            self.vector_store.add_embeddings(texts, embeddings)

            return {
                "status": "success",
                "processed_documents": len(documents),
                "processed_chunks": len(chunks),
                "message": "Documents processed and stored successfully",
            }

        except Exception as e:
            error_message = f"Error processing documents: {str(e)}"
            print(error_message)
            return {"status": "error", "message": error_message}

    async def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        クエリに基づいて関連ドキュメントを検索する

        Args:
            query: 検索クエリ
            top_k: 返す結果の最大数

        Returns:
            検索結果のリスト。各結果は辞書形式で、テキストと類似度スコアを含む
        """
        try:
            # クエリの埋め込みを生成
            query_embedding = embed_query(query, self.embeddings)

            # 類似度検索の実行
            results = self.vector_store.similarity_search(query_embedding, k=top_k)

            # 結果の整形
            formatted_results = [
                {
                    "text": text,
                    "similarity": float(
                        score
                    ),  # np.float32をJSONシリアライズ可能なfloatに変換
                }
                for text, score in results
            ]

            return formatted_results

        except Exception as e:
            print(f"Error during search: {e}")
            raise

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
            # メタデータがない場合は空の辞書を使用
            doc_metadata = metadata if metadata is not None else {}
            document = Document(page_content=content, metadata=doc_metadata)

            # ドキュメントの分割 (単一ドキュメントをリストとして渡す)
            print("Splitting content into chunks...")
            chunks = split_documents([document])  # split_documentsはリストを受け取る
            if not chunks:
                return {
                    "status": "no_chunks",
                    "message": "No chunks created from the content",
                }

            # テキストとメタデータの抽出 (現状メタデータはDBに保存しないが、将来のために抽出はしておく)
            texts = [chunk.page_content for chunk in chunks]
            # chunk_metadata = [chunk.metadata for chunk in chunks] # 必要に応じて利用

            # 埋め込みの生成
            print("Generating embeddings...")
            embeddings = embed_texts(texts, self.embeddings)

            # ベクトルDBへの保存
            print("Storing embeddings in the vector database...")
            # 現状のadd_embeddingsはテキストと埋め込みのみ受け取る
            self.vector_store.add_embeddings(texts, embeddings)

            return {
                "status": "success",
                "processed_chunks": len(chunks),
                "message": "Content processed and stored successfully",
            }

        except Exception as e:
            error_message = f"Error processing content: {str(e)}"
            print(error_message)
            return {"status": "error", "message": error_message}

    def close(self):
        """リソースの解放"""
        if hasattr(self, "vector_store"):
            self.vector_store.close()
