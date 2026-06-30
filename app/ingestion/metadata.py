from hashlib import sha256
from pathlib import Path

from langchain_core.documents import Document


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_doc_id(path: Path) -> str:
    return sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:16]


def chunk_id(doc_id: str, chunk_index: int, content: str) -> str:
    content_digest = sha256(content.encode("utf-8")).hexdigest()[:16]
    return f"{doc_id}:{chunk_index:05d}:{content_digest}"


def add_document_metadata(documents: list[Document], path: Path) -> list[Document]:
    doc_id = stable_doc_id(path)
    source_hash = file_hash(path)
    enriched: list[Document] = []
    for doc in documents:
        metadata = dict(doc.metadata)
        metadata.update(
            {
                "doc_id": doc_id,
                "source_hash": source_hash,
            }
        )
        enriched.append(Document(page_content=doc.page_content, metadata=metadata))
    return enriched
