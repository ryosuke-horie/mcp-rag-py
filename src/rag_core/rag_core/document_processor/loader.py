# rag_core/document_processor/loader.py
import os
from collections.abc import Callable

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

# .txt と .md ファイルを読み込むためのローダー設定
DEFAULT_LOADERS: dict[str, Callable] = {
    ".txt": lambda path: TextLoader(path, encoding="utf-8"),
    ".md": lambda path: TextLoader(path, encoding="utf-8"),
}


def load_documents(
    directory_path: str,
    glob_pattern: str = "**/*",
    custom_loaders: dict[str, Callable] | None = None,
    show_progress: bool = False,
    use_multithreading: bool = False,
    max_concurrency: int | None = None,
) -> list[Document]:
    """
    指定されたディレクトリからドキュメントを読み込みます。
    デフォルトでは .txt と .md ファイルを対象とします。

    Args:
        directory_path: ドキュメントが格納されているディレクトリのパス。
        glob_pattern: 読み込むファイルをフィルタリングするためのglobパターン。
                      デフォルトはサブディレクトリを含む全てのファイル。
        custom_loaders: ファイル拡張子とローダー関数のマッピング。
                        指定しない場合はデフォルトのローダー (.txt, .md) を使用。
        show_progress: 読み込み中に進捗バーを表示するかどうか。
        use_multithreading: 読み込みにマルチスレッドを使用するかどうか。
        max_concurrency: マルチスレッド使用時の最大同時実行数。

    Returns:
        読み込まれたドキュメントのリスト。
    """
    if not os.path.isdir(directory_path):
        raise ValueError(
            f"指定されたパスはディレクトリではありません: {directory_path}"
        )

    loaders_to_use = custom_loaders if custom_loaders is not None else DEFAULT_LOADERS

    loader = DirectoryLoader(
        directory_path,
        glob=glob_pattern,
        use_multithreading=use_multithreading,
        max_concurrency=max_concurrency,
        show_progress=show_progress,
        loader_kwargs={"encoding": "utf-8"},
        silent_errors=True,
    )

    print(f"ドキュメントを読み込み中: {directory_path} (glob: {glob_pattern})")
    docs = loader.load()
    print(f"読み込み完了: {len(docs)}個のドキュメント")

    allowed_extensions = tuple(loaders_to_use.keys())
    filtered_docs = [
        doc
        for doc in docs
        if "source" in doc.metadata
        and doc.metadata["source"].endswith(allowed_extensions)
    ]
    print(
        f"拡張子でフィルタリング後: {len(filtered_docs)}個のドキュメント (拡張子: {allowed_extensions})"
    )

    return filtered_docs


if __name__ == "__main__":
    # テスト用のディレクトリとファイルを作成 (カレントディレクトリに作成)
    TEST_DIR = "temp_docs_for_loader_test"
    os.makedirs(os.path.join(TEST_DIR, "subdir"), exist_ok=True)
    with open(os.path.join(TEST_DIR, "doc1.txt"), "w", encoding="utf-8") as f:
        f.write("これはテストドキュメント1です。")
    with open(os.path.join(TEST_DIR, "doc2.md"), "w", encoding="utf-8") as f:
        f.write("# テストドキュメント2\n\nマークダウン形式です。")
    with open(os.path.join(TEST_DIR, "subdir", "doc3.txt"), "w", encoding="utf-8") as f:
        f.write("サブディレクトリ内のドキュメント。")
    with open(os.path.join(TEST_DIR, "other.log"), "w", encoding="utf-8") as f:
        f.write("これはログファイルです。")  # これは読み込まれないはず

    print(f"--- Running loader test in '{TEST_DIR}' ---")
    try:
        # デフォルト (.txt, .md) の読み込みテスト
        loaded_docs = load_documents(
            TEST_DIR, glob_pattern="**/*[.md|.txt]"
        )  # globで拡張子を指定
        print("\n--- Loaded Documents (Default) ---")
        for doc in loaded_docs:
            print(f"Source: {doc.metadata.get('source', 'N/A')}")
            print(f"Content: {doc.page_content[:50]}...")  # 最初の50文字表示
            print("-" * 10)

        # 想定: doc1.txt, doc2.md, doc3.txt の3つが読み込まれる

    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        # テスト用ディレクトリとファイルを削除
        import shutil

        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
            print(f"\n--- Cleaned up test directory '{TEST_DIR}' ---")
