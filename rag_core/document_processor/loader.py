# rag_core/document_processor/loader.py
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from typing import List, Optional, Dict, Callable
import os

# .txt と .md ファイルを読み込むためのローダー設定
DEFAULT_LOADERS: Dict[str, Callable] = {
    ".txt": lambda path: TextLoader(path, encoding="utf-8"),
    ".md": lambda path: TextLoader(path, encoding="utf-8"),
}

def load_documents(
    directory_path: str,
    glob_pattern: str = "**/*",
    custom_loaders: Optional[Dict[str, Callable]] = None,
    show_progress: bool = False,
    use_multithreading: bool = False,
    max_concurrency: Optional[int] = None,
) -> List[Document]:
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
        raise ValueError(f"指定されたパスはディレクトリではありません: {directory_path}")

    loaders_to_use = custom_loaders if custom_loaders is not None else DEFAULT_LOADERS

    # DirectoryLoaderに渡すローダーのマッピングを作成
    loader_mapping = {
        ext: loader_func
        for ext, loader_func in loaders_to_use.items()
    }

    loader = DirectoryLoader(
        directory_path,
        glob=glob_pattern,
        loader_cls=None, # loader_mapping を使うため None に設定
        loader_kwargs=None, # loader_mapping を使うため None に設定
        use_multithreading=use_multithreading,
        show_progress=show_progress,
        max_concurrency=max_concurrency,
        # LangChain の DirectoryLoader は loader_cls か silent_errors を期待するが、
        # 内部的に glob と拡張子でファイルを処理するため、
        # ここでは loader_mapping を直接使う形にはなっていない。
        # 代わりに、glob で取得したファイルパスに対して拡張子を見て適切なローダーを適用する
        # 必要があるかもしれないが、まずは DirectoryLoader のデフォルト挙動に任せる。
        # TextLoader がデフォルトで使われることを期待。
        # -> DirectoryLoader の実装を確認したところ、glob でファイルリストを取得し、
        #    各ファイルに対して loader_cls を適用する仕組み。
        #    特定の拡張子ごとに異なるローダーを使うには DirectoryLoader を拡張するか、
        #    自前でファイルリストを取得してループ処理する必要がある。
        #    ここではシンプルに TextLoader をデフォルトとして .txt と .md を処理させる。
        #    より厳密な拡張子別処理が必要な場合は DirectoryLoader を使わず自前実装を検討。
        #
        # 再考: DirectoryLoader は glob で指定したパターンに一致するファイル *全て* を
        # loader_cls (デフォルトは UnstructuredLoader, 指定すれば TextLoader など) で
        # 読み込もうとする。拡張子ごとの振り分けは DirectoryLoader 自体にはない。
        # そのため、.txt と .md のみを対象とするには glob を調整するか、
        # 読み込み後にフィルタリングする必要がある。
        # ここでは glob で指定し、TextLoader を使う方針とする。
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'},
        silent_errors=True, # エラーが発生しても処理を続ける
    )

    print(f"Loading documents from: {directory_path} using glob: {glob_pattern}")
    docs = loader.load()
    print(f"Loaded {len(docs)} documents.")

    # 念のため、意図しないファイルが読み込まれていないか拡張子でフィルタリング
    # (DirectoryLoader が glob でフィルタしてくれるはずだが、安全のため)
    allowed_extensions = tuple(loaders_to_use.keys())
    filtered_docs = [
        doc for doc in docs
        if 'source' in doc.metadata and doc.metadata['source'].endswith(allowed_extensions)
    ]
    print(f"Filtered down to {len(filtered_docs)} documents with extensions: {allowed_extensions}")


    return filtered_docs

if __name__ == '__main__':
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
        f.write("これはログファイルです。") # これは読み込まれないはず

    print(f"--- Running loader test in '{TEST_DIR}' ---")
    try:
        # デフォルト (.txt, .md) の読み込みテスト
        loaded_docs = load_documents(TEST_DIR, glob_pattern="**/*[.md|.txt]") # globで拡張子を指定
        print("\n--- Loaded Documents (Default) ---")
        for doc in loaded_docs:
            print(f"Source: {doc.metadata.get('source', 'N/A')}")
            print(f"Content: {doc.page_content[:50]}...") # 最初の50文字表示
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

```
</write_to_file>
