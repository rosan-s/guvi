from pydantic import BaseModel
from dotenv import load_dotenv
import os

_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(_env_path)


class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///finance.db")
    api_key: str = os.getenv("API_KEY", "dev-key")
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "*").split(",")
        if origin.strip()
    ]


settings = Settings()
