"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global configuration settings for Simpson Strong-Tie MCP."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(default="local", description="Runtime environment")
    debug: bool = Field(default=True, description="Debug mode")
    log_level: str = Field(default="INFO", description="Log level")

    # PostgreSQL configuration
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="simpson_mcp")
    postgres_user: str = Field(default="simpson")
    postgres_password: str = Field(default="simpson_dev_password")
    database_url: str = Field(
        default="postgresql+asyncpg://simpson:simpson_dev_password@localhost:5432/simpson_mcp"
    )

    # Object storage configuration
    storage_adapter: str = Field(default="filesystem", description="filesystem or minio")
    storage_local_root: str = Field(default="./data/storage")
    minio_endpoint: str = Field(default="http://localhost:9000")
    minio_access_key: str = Field(default="minioadmin")
    minio_secret_key: str = Field(default="minioadmin")
    minio_bucket: str = Field(default="simpson-evidence")

    # Port configuration
    api_port: int = Field(default=8000)
    mcp_port: int = Field(default=8001)
    admin_web_port: int = Field(default=5173)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
