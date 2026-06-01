from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "BankGuard API"
    DESCRIPTION: str = (
        "A fraud detection API for banking transactions "
        "powered by XGBoost, SHAP, FastAPI, and PostgreSQL."
    )
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/bankguard"
    DEBUG: bool = True

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()