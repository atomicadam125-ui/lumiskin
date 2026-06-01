from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Skincare Analysis API"
    environment: str = "local"
    debug: bool = False
    secret_key: str = Field(min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    database_url: str = "sqlite+pysqlite:///./preview.db"
    local_upload_dir: str = "local_uploads"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    apple_client_ids: list[str] = []
    cors_origins: list[str] = ["http://localhost:19006", "http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("apple_client_ids", mode="before")
    @classmethod
    def parse_apple_client_ids(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [client_id.strip() for client_id in value.split(",") if client_id.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
