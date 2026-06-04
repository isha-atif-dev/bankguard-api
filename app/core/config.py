"""
config.py

Central configuration file for the BankGuard API.

All project settings are defined here in one place.
Other files import the settings object to access these values
instead of hardcoding them across multiple files.

Secret values like real database passwords should be stored
in a .env file which Pydantic reads automatically.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "BankGuard API"
    DESCRIPTION: str = (
        "A fraud detection API for banking transactions "
        "powered by XGBoost, SHAP, FastAPI, and PostgreSQL."
    )
    VERSION: str = "1.0.0"
    # Database connection URL. Replace with real credentials in .env file.
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/bankguard"
    DEBUG: bool = True   # True means development mode with detailed errors.
    
    # Reading secret values from .env file automatically.
    model_config = {"env_file": ".env", "case_sensitive": True}

# settings object imported by all other files.
settings = Settings()