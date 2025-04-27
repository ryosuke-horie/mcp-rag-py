# rag_core/document_processor/splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Optional

def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    length_function: callable = len,
    is_separator_regex: bool = False,
    separators: Optional[List[str]] = None,
    keep_separator: bool = True,
    **kwargs
) -> List[Document]:
    """
    与えられたドキュメントリストをチャンクに分割します。

    Args:
        documents: 分割対象の Document オブジェクトのリスト。
        chunk_size: 各チャンクの最大サイズ。
        chunk_overlap: チャンク間のオーバーラップサイズ。
        length_function: チャンクサイズを計算するための関数。
        is_separator_regex: separators が正規表現かどうか。
        separators: テキストを分割するためのセパレータのリスト。
                    指定しない場合は RecursiveCharacterTextSplitter のデフォルトを使用。
        keep_separator: 分割後もセパレータを保持するかどうか。
        **kwargs: RecursiveCharacterTextSplitter に渡すその他の引数。

    Returns:
        分割された Document オブジェクトのリスト。
    """
    if separators is None:
        # RecursiveCharacterTextSplitter のデフォルトセパレータを使用
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
            is_separator_regex=is_separator_regex,
            keep_separator=keep_separator,
            **kwargs
        )
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            keep_separator=keep_separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
            is_separator_regex=is_separator_regex,
            **kwargs
        )

    print(f"Splitting {len(documents)} documents into chunks (size={chunk_size}, overlap={chunk_overlap})...")
    split_docs = text_splitter.split_documents(documents)
    print(f"Split into {len(split_docs)} chunks.")

    return split_docs

if __name__ == '__main__':
    # テスト用のダミードキュメントを作成
    long_text = """これは非常に長いテストドキュメントです。
    複数の段落に分かれています。RecursiveCharacterTextSplitter は、
    まず改行2つ（\\n\\n）で分割しようとします。
    それでもチャンクサイズを超える場合は、次に改行1つ（\\n）で分割します。
    さらにスペース（ ）で分割し、最終的には文字単位（""）で分割します。
    これにより、意味のあるまとまりを可能な限り維持しようとします。

    チャンクサイズを100、オーバーラップを20としてテストしてみましょう。
    オーバーラップは、チャンク間の文脈を維持するのに役立ちます。
    例えば、前のチャンクの最後の部分が、次のチャンクの最初の部分に含まれます。

    This is a very long test document.
    It is divided into multiple paragraphs. RecursiveCharacterTextSplitter
    first tries to split by double newlines (\\n\\n).
    If it still exceeds the chunk size, it then splits by single newlines (\\n).
    Then by spaces ( ), and finally by characters ("").
    This attempts to keep semantically related pieces of text together as much as possible.

    Let's test with a chunk size of 100 and an overlap of 20.
    Overlap helps maintain context between chunks.
    For example, the end of the previous chunk is included at the beginning of the next chunk.
    """ * 5 # テキストを長くするために5回繰り返す

    dummy_doc = Document(page_content=long_text, metadata={"source": "dummy_test_doc"})
    dummy_docs = [dummy_doc]

    print("--- Running splitter test ---")
    try:
        # デフォルト設定 (chunk_size=1000, chunk_overlap=200) で分割
        print("\n--- Splitting with default settings ---")
        split_docs_default = split_documents(dummy_docs)
        print(f"Number of chunks (default): {len(split_docs_default)}")
        # 最初のチャンクの内容を一部表示
        if split_docs_default:
            print("First chunk (default):")
            print(f"Source: {split_docs_default[0].metadata.get('source', 'N/A')}")
            print(f"Content: {split_docs_default[0].page_content[:150]}...")

        # カスタム設定 (chunk_size=100, chunk_overlap=20) で分割
        print("\n--- Splitting with custom settings (size=100, overlap=20) ---")
        split_docs_custom = split_documents(dummy_docs, chunk_size=100, chunk_overlap=20)
        print(f"Number of chunks (custom): {len(split_docs_custom)}")
        # 最初のチャンクの内容を一部表示
        if split_docs_custom:
            print("First chunk (custom):")
            print(f"Source: {split_docs_custom[0].metadata.get('source', 'N/A')}")
            print(f"Content: {split_docs_custom[0].page_content[:150]}...") # チャンクサイズが小さいので全体が表示されるかも

    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        print("\n--- Splitter test finished ---")
