from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from app.core.config import Settings, get_settings
from app.ingestion.embed import build_embeddings


def get_vector_store(
    settings: Settings | None = None,
    embeddings: Embeddings | None = None,
) -> Chroma:
    settings = settings or get_settings()
    settings.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=embeddings or build_embeddings(settings),
        persist_directory=str(settings.chroma_persist_dir),
    )


def delete_existing_source(vector_store: Chroma, source_path: Path) -> None:
    try:
        vector_store._collection.delete(where={"source_path": str(source_path.resolve())})
    except Exception:
        # Chroma raises on an empty delete in some versions. Replacement ingestion can proceed.
        pass


def index_chunks(vector_store: Chroma, chunks: list[Document]) -> int:
    if not chunks:
        return 0
    ids = [doc.metadata["chunk_id"] for doc in chunks]
    vector_store.add_documents(chunks, ids=ids)
    return len(chunks)
