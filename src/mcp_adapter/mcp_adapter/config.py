"""MCP Adapter configuration module."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """MCP Adapter settings."""

    model_config = SettingsConfigDict(env_prefix="MCP_ADAPTER_", env_file=".env")

    # MCP server settings
    server_name: str = "RAG MCP Adapter"
    
    # RAG API Server settings
    rag_api_base_url: str = "http://localhost:8000"
    
    # Server settings
    host: str = "localhost"
    port: int = 8080
    log_level: str = "info"


settings = Settings()
