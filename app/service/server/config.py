import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI-Test Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    API_KEY: str = ""

    CACHE_MAX_ENTRIES: int = 100
    CACHE_TTL_SECONDS: int = 3600

    CORS_ORIGINS: list[str] = ["*"]

    LOG_LEVEL: str = "INFO"

    MAX_UPLOAD_SIZE_MB: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
