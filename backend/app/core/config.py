"""Configuration management for the backend application."""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database - use SQLite for local development if no DATABASE_URL provided
    DATABASE_URL: str = "sqlite:///./todo.db"

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7
    BETTER_AUTH_SECRET: str = "your-secret-key-here"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,https://*.vercel.app,https://*.vercel.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
