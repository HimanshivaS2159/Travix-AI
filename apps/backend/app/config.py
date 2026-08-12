"""
Application Configuration
Manages environment variables and settings
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # API Configuration
    environment: str = "development"
    port: int = 8000
    host: str = "0.0.0.0"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Groq API Configuration
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    
    # Database Configuration
    database_url: str = "postgresql://travix:travix_password@postgres:5432/travix_db"
    
    # Redis Configuration
    redis_url: str = "redis://redis:6379"
    
    # Agent Configuration
    orchestrator_system_prompt: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
