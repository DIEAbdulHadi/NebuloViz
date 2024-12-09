
import os
from pydantic import BaseSettings, Field
from typing import List


class BaseSettingsConfig(BaseSettings):
    """Base configuration with common settings."""

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PASSWORD_HASH_SALT: str = Field(..., env="PASSWORD_HASH_SALT")
    EMAIL_SMTP_SERVER: str = Field(..., env="EMAIL_SMTP_SERVER")
    EMAIL_SMTP_PORT: int = Field(..., env="EMAIL_SMTP_PORT")
    EMAIL_USERNAME: str = Field(..., env="EMAIL_USERNAME")
    EMAIL_PASSWORD: str = Field(..., env="EMAIL_PASSWORD")
    NOTIFICATION_RECIPIENTS: List[str] = Field(..., env="NOTIFICATION_RECIPIENTS")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    SUPPORTED_LANGUAGES: List[str] = ["en", "es", "fr"]
    DEFAULT_LANGUAGE: str = "en"
    RATE_LIMIT: str = "100/minute"  # For rate limiting
    CACHE_NAMESPACE: str = Field("nebuloviz_dev", env="CACHE_NAMESPACE")
    KAFKA_BOOTSTRAP_SERVERS: str = Field(..., env="KAFKA_BOOTSTRAP_SERVERS")
    AI_MODELS_PATH: str = "./models/"
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentSettings(BaseSettingsConfig):
    """Development environment settings."""

    ENVIRONMENT: str = "development"
    CACHE_NAMESPACE: str = "nebuloviz_dev"


class ProductionSettings(BaseSettingsConfig):
    """Production environment settings."""

    ENVIRONMENT: str = "production"
    CACHE_NAMESPACE: str = "nebuloviz_prod"


def get_settings():
    """Retrieves the appropriate settings based on the ENVIRONMENT variable."""
    if os.getenv('ENVIRONMENT') == 'production':
        return ProductionSettings()
    return DevelopmentSettings()


settings = get_settings()
