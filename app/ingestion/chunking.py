from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import Settings
from app.ingestion.metadata import chunk_id


def split_documents(documents: list[Document], settings: Settings) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", "; ", ", ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    for index, doc in enumerate(chunks):
        doc.metadata["chunk_index"] = index
        doc.metadata["chunk_id"] = chunk_id(doc.metadata["doc_id"], index, doc.page_content)
    return chunks
