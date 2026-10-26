from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Indian Market Morning Scanner"
    app_env: str = "development"
    database_url: str = "sqlite:///./market_scanner.db"
    redis_host: str = "localhost"
    redis_port: int = 6379
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    anthropic_api_key: str = "changeme"
    firebase_project_id: str = "changeme"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
