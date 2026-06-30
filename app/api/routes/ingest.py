from pathlib import Path

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.schemas import IngestRequest, IngestResponse
from app.ingestion.pipeline import ingest_path

router = APIRouter()


@router.post("", response_model=IngestResponse)
def ingest(request: IngestRequest) -> IngestResponse:
    settings = get_settings()
    path = Path(request.path) if request.path else settings.raw_pdf_dir
    documents = ingest_path(path=path, glob=request.glob)
    return IngestResponse(
        documents=documents,
        total_chunks=sum(doc.chunks for doc in documents),
    )
