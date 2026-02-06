from pydantic import BaseModel
from dotenv import load_dotenv
import os

_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(_env_path)


class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/finhealth")
    api_key: str = os.getenv("API_KEY", "dev-key")
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


settings = Settings()
