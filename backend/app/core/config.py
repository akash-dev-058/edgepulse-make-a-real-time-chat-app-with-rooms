import os
from typing import List
from pydantic import AnyHttpUrl, BaseSettings, validator

class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    SERVE_STATIC: bool = False

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "RS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Socket.IO
    SOCKET_IO_SECRET: str

    # Security
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    # Email
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = "noreply@chatapp.com"

    # Sentry
    SENTRY_DSN: str = ""

    # Auth
    NEXTAUTH_SECRET: str = ""
    NEXTAUTH_URL: str = "http://localhost:3000"

    # Rate limiting
    RATE_LIMIT: int = 100

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [url.strip() for url in v.split(",")]
        return v

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"

settings = Settings()
