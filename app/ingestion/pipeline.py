import logging
from pathlib import Path

from app.core.config import Settings, get_settings
from app.core.schemas import IngestedDocument
from app.ingestion.chunking import split_documents
from app.ingestion.index import delete_existing_source, get_vector_store, index_chunks
from app.ingestion.loaders import discover_pdfs, load_pdf
from app.ingestion.metadata import add_document_metadata, stable_doc_id
from app.ingestion.preprocess import clean_documents

logger = logging.getLogger(__name__)


def ingest_pdf(path: Path, settings: Settings | None = None) -> IngestedDocument:
    settings = settings or get_settings()
    path = path.resolve()
    logger.info("Loading PDF: %s", path)
    pages = load_pdf(path)
    cleaned = clean_documents(pages)
    enriched = add_document_metadata(cleaned, path)
    chunks = split_documents(enriched, settings)

    vector_store = get_vector_store(settings)
    delete_existing_source(vector_store, path)
    indexed_count = index_chunks(vector_store, chunks)

    return IngestedDocument(
        source_file=path.name,
        doc_id=stable_doc_id(path),
        pages=len(pages),
        chunks=indexed_count,
    )


def ingest_path(path: Path | None = None, glob: str = "*.pdf") -> list[IngestedDocument]:
    settings = get_settings()
    root = (path or settings.raw_pdf_dir).resolve()
    pdfs = discover_pdfs(root, glob=glob)
    if not pdfs:
        logger.warning("No PDFs found at %s with glob %s", root, glob)
        return []
    return [ingest_pdf(pdf, settings) for pdf in pdfs]
