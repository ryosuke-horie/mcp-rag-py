# rag_core/document_processor/splitter.py

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    length_function: callable = len,
    is_separator_regex: bool = False,
    separators: list[str] | None = None,
    keep_separator: bool = True,
    **kwargs,
) -> list[Document]:
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
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
            is_separator_regex=is_separator_regex,
            keep_separator=keep_separator,
            **kwargs,
        )
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            keep_separator=keep_separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
            is_separator_regex=is_separator_regex,
            **kwargs,
        )

    print(
        f"ドキュメントを分割中... (チャンクサイズ={chunk_size}, オーバーラップ={chunk_overlap})"
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"分割完了: {len(split_docs)}個のチャンクに分割されました。")

    return split_docs


if __name__ == "__main__":
    # テスト用のダミードキュメントを作成
    long_text = (
        """これは非常に長いテストドキュメントです。
    複数の段落に分かれています。RecursiveCharacterTextSplitter は、
    まず改行2つ（\\n\\n）で分割しようとします。
    それでもチャンクサイズを超える場合は、次に改行1つ（\\n）で分割します。
    さらにスペース（ ）で分割し、最終的には文字単位（""）で分割します。
    これにより、意味のあるまとまりを可能な限り維持しようとします。

    チャンクサイズを100、オーバーラップを20としてテストしてみましょう。
    オーバーラップは、チャンク間の文脈を維持するのに役立ちます。
    例えば、前のチャンクの最後の部分が、次のチャンクの最初の部分に含まれます。
    """
        * 5
    )

    dummy_doc = Document(page_content=long_text, metadata={"source": "dummy_test_doc"})
    dummy_docs = [dummy_doc]

    print("--- 分割テスト開始 ---")
    try:
        # デフォルト設定 (chunk_size=1000, chunk_overlap=200) で分割
        print("\n--- デフォルト設定での分割 ---")
        split_docs_default = split_documents(dummy_docs)
        print(f"チャンク数 (デフォルト): {len(split_docs_default)}")
        if split_docs_default:
            print("最初のチャンク (デフォルト):")
            print(f"ソース: {split_docs_default[0].metadata.get('source', 'N/A')}")
            print(f"内容: {split_docs_default[0].page_content[:150]}...")

        # カスタム設定 (chunk_size=100, chunk_overlap=20) で分割
        print("\n--- カスタム設定での分割 (サイズ=100, オーバーラップ=20) ---")
        split_docs_custom = split_documents(
            dummy_docs, chunk_size=100, chunk_overlap=20
        )
        print(f"チャンク数 (カスタム): {len(split_docs_custom)}")
        if split_docs_custom:
            print("最初のチャンク (カスタム):")
            print(f"ソース: {split_docs_custom[0].metadata.get('source', 'N/A')}")
            print(f"内容: {split_docs_custom[0].page_content[:150]}...")

    except Exception as e:
        print(f"テスト中にエラーが発生しました: {e}")
    finally:
        print("\n--- 分割テスト終了 ---")
