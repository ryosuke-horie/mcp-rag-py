# Ollamaを使用した埋め込みモデルの実装
import os

from langchain_ollama import OllamaEmbeddings


def initialize_embedding_model(
    ollama_base_url: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
    model_name: str = os.environ.get("EMBEDDING_MODEL_NAME", "bge-m3"),
) -> OllamaEmbeddings:
    """
    Ollama埋め込みモデルのインスタンスを初期化して返します。

    環境変数からOllamaのベースURLとモデル名を読み取り、
    デフォルト値を使用します。

    Args:
        ollama_base_url (str): OllamaサーバーのベースURL。
                               デフォルトは"http://localhost:11434"またはOLLAMA_BASE_URL環境変数。
        model_name (str): 使用する埋め込みモデルの名前。
                         デフォルトは"bge-m3"またはEMBEDDING_MODEL_NAME環境変数。

    Returns:
        OllamaEmbeddings: Ollama埋め込みモデルのインスタンス。
    """
    print(
        f"Ollama埋め込みモデルを初期化中: base_url='{ollama_base_url}', model='{model_name}'"
    )
    embeddings = OllamaEmbeddings(base_url=ollama_base_url, model=model_name)
    return embeddings


def embed_texts(texts: list[str], embeddings: OllamaEmbeddings) -> list[list[float]]:
    """
    指定されたOllama埋め込みモデルを使用してテキストリストを埋め込みます。

    Args:
        texts (List[str]): 埋め込むテキストのリスト。
        embeddings (OllamaEmbeddings): 初期化されたOllama埋め込みモデルのインスタンス。

    Returns:
        List[List[float]]: 各入力テキストに対する埋め込みベクトルのリスト。
    """
    print(f"{len(texts)}個のドキュメントを埋め込み中...")
    embedded_vectors = embeddings.embed_documents(texts)
    print("埋め込み完了。")
    return embedded_vectors


def embed_query(text: str, embeddings: OllamaEmbeddings) -> list[float]:
    """
    指定されたOllama埋め込みモデルを使用して単一のクエリテキストを埋め込みます。

    Args:
        text (str): 埋め込むクエリテキスト。
        embeddings (OllamaEmbeddings): 初期化されたOllama埋め込みモデルのインスタンス。

    Returns:
        List[float]: 入力クエリテキストの埋め込みベクトル。
    """
    print(f"クエリを埋め込み中: '{text[:50]}...'")  # 最初の50文字をログに記録
    embedded_vector = embeddings.embed_query(text)
    print("クエリの埋め込み完了。")
    return embedded_vector


# 使用例（オプション、テスト用）
if __name__ == "__main__":
    # Ollamaサーバーが実行中で、モデルが利用可能であることを確認
    # 例: ollama run bge-m3

    # 必要に応じて環境変数を設定（またはデフォルト値に依存）
    # os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    # os.environ["EMBEDDING_MODEL_NAME"] = "bge-m3"

    try:
        print("--- 埋め込みモデルのテスト ---")
        embedding_model = initialize_embedding_model()

        # ドキュメントの埋め込みをテスト
        sample_texts = [
            "これは最初のドキュメントです。",
            "このドキュメントは2番目のドキュメントです。",
            "そしてこれは3番目のドキュメントです。",
            "これは最初のドキュメントですか？",
        ]
        vectors = embed_texts(sample_texts, embedding_model)
        print(f"{len(vectors)}個のベクトルを生成しました。")
        if vectors:
            print(f"最初のベクトルの次元: {len(vectors[0])}")
            # print("最初のベクトル（最初の10次元）:", vectors[0][:10]) # コメントを外すとベクトルの一部を表示

        print("\n--- クエリの埋め込みテスト ---")
        # クエリの埋め込みをテスト
        query = "2番目のドキュメントは何について書かれていますか？"
        query_vector = embed_query(query, embedding_model)
        print(f"クエリベクトルを生成しました。次元: {len(query_vector)}")
        # print("クエリベクトル（最初の10次元）:", query_vector[:10]) # コメントを外すとベクトルの一部を表示

        print("\n--- 埋め込みテスト成功 ---")

    except Exception as e:
        print("\n--- 埋め込みテスト失敗 ---")
        print(f"エラーが発生しました: {e}")
        print(
            "Ollamaサーバーが実行中で、指定されたモデル（デフォルトは'bge-m3'）が利用可能であることを確認してください。"
        )
        print("ターミナルで'ollama run bge-m3'を実行する必要があるかもしれません。")
