"""
Configuration settings for the backend application
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # App Config
    APP_NAME: str = "Housing Intelligence Platform - Backend"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    PORT: int = 8000

    # Database Config
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str = "housing_intelligence"

    # AI-Engine Config
    AI_ENGINE_URL: str = "http://localhost:8001"

    # Cloudinary Config
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # CORS Config
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    @property
    def DATABASE_URL(self) -> str:
        """Construct MySQL database URL"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
