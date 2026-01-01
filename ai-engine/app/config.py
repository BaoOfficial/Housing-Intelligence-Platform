"""
Configuration settings for the AI Engine
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """AI Engine settings"""

    # App Config
    APP_NAME: str = "Housing Intelligence Platform - AI Engine"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    PORT: int = 8001

    # Backend API Config
    BACKEND_URL: str = "http://localhost:8000"

    # ChromaDB Config (Embedded Mode)
    CHROMADB_COLLECTION: str = "tenant_reviews"

    # OpenAI Config
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.7

    # CORS Config
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
