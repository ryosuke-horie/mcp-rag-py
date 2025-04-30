"""設定モジュール"""

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定"""

    # RAG APIサーバーの設定
    rag_api_base_url: str = "http://localhost:8000"

    # サーバーの設定
    host: str = "0.0.0.0"
    port: int = 8001

    # ログ設定
    log_level: str = "INFO"
    log_file: str | None = None

    # モデル設定
    model_config = SettingsConfigDict(
        env_file=os.path.join(Path(__file__).parent.parent.parent, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# グローバル設定インスタンス
settings = Settings()
