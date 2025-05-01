import logging
from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
)
from langchain_core.documents import Document

from .document_processor.loader import load_documents
from .document_processor.splitter import split_documents
from .embedding.model import initialize_embedding_model
from .vectordb.storage import DuckDBVectorStore

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def _process_and_store_documents(docs: list[Document], storage: DuckDBVectorStore):
    """ドキュメントのリストを処理し、ベクトルDBに保存する共通関数"""
    if not docs:
        logging.warning("処理対象のドキュメントが見つかりませんでした。")
        return

    logging.info(
        f"{len(docs)} 個のドキュメントを読み込みました。チャンク分割を開始します..."
    )
    chunks = split_documents(docs)
    logging.info(f"{len(chunks)} 個のチャンクに分割しました。ベクトル化を開始します...")

    embedding_model = initialize_embedding_model()
    try:
        chunk_texts = [chunk.page_content for chunk in chunks]
        logging.info(f"{len(chunk_texts)} 個のチャンクのベクトル化を実行します...")
        embeddings = embedding_model.embed_documents(chunk_texts)
        logging.info("ベクトル化が完了しました。データベースへの保存を開始します...")
        storage.add_embeddings(texts=chunk_texts, embeddings=embeddings)
        logging.info("データベースへの保存が完了しました。")
    except Exception as e:
        logging.error(
            f"ベクトル化またはDB保存中にエラーが発生しました: {e}", exc_info=True
        )


def process_file(file_path: Path):
    """単一のドキュメントファイルを処理してベクトルDBに登録する"""
    logging.info(f"ファイル処理を開始: {file_path}")
    storage = DuckDBVectorStore()
    try:
        # TextLoaderを使用して単一ファイルを読み込む
        loader = TextLoader(str(file_path), encoding="utf-8")
        docs = loader.load()
        doc = docs[0] if docs else None
        if doc:
            _process_and_store_documents([doc], storage)
        else:
            logging.warning(f"ファイルの読み込みに失敗しました: {file_path}")
    except Exception as e:
        logging.error(
            f"ファイル処理中にエラーが発生しました ({file_path}): {e}", exc_info=True
        )
    finally:
        storage.close()
        logging.info(f"ファイル処理を終了: {file_path}")


def process_directory(directory_path: Path):
    """指定されたディレクトリ内のドキュメントを再帰的に処理してベクトルDBに登録する"""
    logging.info(f"ディレクトリ処理を開始: {directory_path}")
    storage = DuckDBVectorStore()
    try:
        docs = load_documents(str(directory_path))
        _process_and_store_documents(docs, storage)
    except Exception as e:
        logging.error(
            f"ディレクトリ処理中にエラーが発生しました ({directory_path}): {e}",
            exc_info=True,
        )
    finally:
        storage.close()
        logging.info(f"ディレクトリ処理を終了: {directory_path}")
