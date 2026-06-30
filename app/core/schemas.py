from pydantic import BaseModel, Field


class Citation(BaseModel):
    source_file: str
    page_number: int | None = None
    policy_name: str | None = None
    section_title: str | None = None
    chunk_id: str | None = None


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)
    filter: dict | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_context: list[dict] = Field(default_factory=list)


class IngestRequest(BaseModel):
    path: str | None = None
    glob: str = "*.pdf"


class IngestedDocument(BaseModel):
    source_file: str
    doc_id: str
    pages: int
    chunks: int


class IngestResponse(BaseModel):
    documents: list[IngestedDocument]
    total_chunks: int
