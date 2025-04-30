from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """APIサーバーの設定"""

    # Ollamaの設定
    ollama_base_url: str = "http://localhost:11434"
    embedding_model_name: str = "bge-m3"

    # DuckDBの設定
    db_path: str = "vector_store.db"
    table_name: str = "embeddings"

    # ドキュメント処理の設定
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # 環境変数のプレフィックス
    class Config:
        env_prefix = "RAG_"


# グローバル設定インスタンス
settings = Settings()
