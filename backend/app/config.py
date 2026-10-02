from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg2://study:study@localhost:5432/study_rag"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7

    # LLM: Groq (console.groq.com) OR xAI Grok (console.x.ai) — not interchangeable
    llm_provider: str = "auto"  # auto | groq | xai
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    xai_api_key: str = ""
    xai_model: str = "grok-build-0.1"
    grok_timeout_seconds: int = 120

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384

    data_dir: Path = Path("./data")
    faiss_dir: Path = Path("./data/faiss")
    upload_dir: Path = Path("./data/uploads")

    retrieval_top_k: int = 5
    coverage_full_threshold: float = 0.75
    coverage_partial_threshold: float = 0.5
    weak_point_error_threshold: float = 0.4

    max_upload_bytes: int = 50 * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.faiss_dir.mkdir(parents=True, exist_ok=True)
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    return settings
