from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    google_cloud_project: str | None = Field(default=None, alias="GOOGLE_CLOUD_PROJECT")
    google_cloud_location: str = Field(default="us-central1", alias="GOOGLE_CLOUD_LOCATION")

    gemini_model: str = Field(default="gemini-2.5-flash", alias="GEMINI_MODEL")
    embedding_model: str = Field(default="text-embedding-005", alias="EMBEDDING_MODEL")

    chroma_persist_dir: Path = Field(default=Path("./data/chroma"), alias="CHROMA_PERSIST_DIR")
    chroma_collection: str = Field(default="policy_documents", alias="CHROMA_COLLECTION")
    raw_pdf_dir: Path = Field(default=Path("./data/raw_pdfs"), alias="RAW_PDF_DIR")

    chunk_size: int = Field(default=1200, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=180, alias="CHUNK_OVERLAP")
    retrieval_top_k: int = Field(default=6, alias="RETRIEVAL_TOP_K")
    retrieval_fetch_k: int = Field(default=20, alias="RETRIEVAL_FETCH_K")
    retrieval_mode: Literal["similarity", "mmr"] = Field(default="mmr", alias="RETRIEVAL_MODE")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
