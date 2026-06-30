from langchain_core.vectorstores import VectorStoreRetriever

from app.core.config import Settings, get_settings
from app.ingestion.index import get_vector_store


def build_retriever(
    settings: Settings | None = None,
    top_k: int | None = None,
    metadata_filter: dict | None = None,
) -> VectorStoreRetriever:
    settings = settings or get_settings()
    vector_store = get_vector_store(settings)
    k = top_k or settings.retrieval_top_k
    search_kwargs: dict = {"k": k}
    if metadata_filter:
        search_kwargs["filter"] = metadata_filter

    if settings.retrieval_mode == "mmr":
        search_kwargs["fetch_k"] = max(settings.retrieval_fetch_k, k)
        return vector_store.as_retriever(search_type="mmr", search_kwargs=search_kwargs)
    return vector_store.as_retriever(search_type="similarity", search_kwargs=search_kwargs)
