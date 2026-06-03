"""Core settings and configuration management for REX AI system."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """REX System Configuration."""
    
    # Project
    PROJECT_NAME: str = "REX AI System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Environment
    REX_ENV: str = Field(default="development", alias="REX_ENV")
    REX_LOG_LEVEL: str = Field(default="INFO", alias="REX_LOG_LEVEL")
    
    # API Configuration
    REX_API_PORT: int = Field(default=5000, alias="REX_API_PORT")
    REX_API_HOST: str = Field(default="0.0.0.0", alias="REX_API_HOST")
    REX_API_TIMEOUT: int = 30
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(default="", alias="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL")
    OPENAI_TEMPERATURE: float = Field(default=0.7, alias="OPENAI_TEMPERATURE")
    OPENAI_MAX_TOKENS: int = 4096
    
    # Security
    REX_PERMISSION_REQUIRED: bool = Field(default=True, alias="REX_PERMISSION_REQUIRED")
    REX_ADMIN_USER: str = Field(default="admin", alias="REX_ADMIN_USER")
    REX_SECRET_KEY: str = Field(default="dev-secret-key-change-in-production", alias="REX_SECRET_KEY")
    
    # Memory Configuration
    REX_MEMORY_TYPE: str = Field(default="hybrid", alias="REX_MEMORY_TYPE")  # hybrid, sqlite, redis
    REX_MEMORY_MAX_ITEMS: int = Field(default=10000, alias="REX_MEMORY_MAX_ITEMS")
    REX_MEMORY_PERSISTENCE: str = Field(default="sqlite", alias="REX_MEMORY_PERSISTENCE")
    
    # Voice Configuration
    REX_VOICE_ENABLED: bool = Field(default=True, alias="REX_VOICE_ENABLED")
    REX_VOICE_ENGINE: str = Field(default="pyttsx3", alias="REX_VOICE_ENGINE")
    REX_VOICE_RATE: int = Field(default=150, alias="REX_VOICE_RATE")
    
    # Self-Modification
    REX_SELF_MODIFY_ENABLED: bool = Field(default=True, alias="REX_SELF_MODIFY_ENABLED")
    REX_CODE_REVIEW_REQUIRED: bool = Field(default=True, alias="REX_CODE_REVIEW_REQUIRED")
    REX_MAX_ITERATIONS: int = Field(default=10, alias="REX_MAX_ITERATIONS")
    
    # Database
    REX_DB_TYPE: str = Field(default="sqlite", alias="REX_DB_TYPE")
    REX_DB_PATH: str = Field(default="data/rex.db", alias="REX_DB_PATH")
    
    # Redis Configuration (optional)
    REDIS_ENABLED: bool = Field(default=False, alias="REDIS_ENABLED")
    REDIS_HOST: str = Field(default="localhost", alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, alias="REDIS_PORT")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False
        extra = "allow"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.REX_ENV.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.REX_ENV.lower() == "production"
    
    def validate_critical_settings(self) -> tuple[bool, str]:
        """Validate critical settings are configured."""
        if not self.OPENAI_API_KEY or self.OPENAI_API_KEY == "your_openai_api_key_here":
            return False, "OPENAI_API_KEY not configured"
        return True, "Configuration valid"


# Global settings instance
settings = Settings()
