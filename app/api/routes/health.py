from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "collection": settings.chroma_collection,
        "chroma_persist_dir": str(settings.chroma_persist_dir),
        "gemini_model": settings.gemini_model,
        "embedding_model": settings.embedding_model,
    }
