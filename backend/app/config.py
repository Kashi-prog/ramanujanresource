"""Application configuration settings."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    app_name: str = "Carbon Shadow Tracker API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Database Configuration
    database_url: str = "sqlite:///./carbon_tracker.db"
    
    # CORS Configuration
    cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Carbon Intensity API (example, could be replaced with real API)
    carbon_intensity_api_key: Optional[str] = None
    default_carbon_intensity: float = 475.0  # gCO2/kWh global average
    
    # Model Configuration
    ml_model_path: str = "./models/"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
