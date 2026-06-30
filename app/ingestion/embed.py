from langchain_google_vertexai import VertexAIEmbeddings

from app.core.config import Settings, get_settings


def build_embeddings(settings: Settings | None = None) -> VertexAIEmbeddings:
    settings = settings or get_settings()
    kwargs = {
        "model": settings.embedding_model,
        "location": settings.google_cloud_location,
    }
    if settings.google_cloud_project:
        kwargs["project"] = settings.google_cloud_project
    return VertexAIEmbeddings(**kwargs)
