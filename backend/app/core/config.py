import os
from typing import List
from pydantic import BaseSettings, PostgresDsn, RedisDsn, Field, AnyUrl

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")
    REDIS_URL: RedisDsn = Field(..., env="REDIS_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    CORS_ORIGINS: List[AnyUrl] = Field(default_factory=list, env="CORS_ORIGINS")
    SENTRY_DSN: str | None = Field(default=None, env="SENTRY_DSN")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
