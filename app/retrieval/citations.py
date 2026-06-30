from langchain_core.documents import Document

from app.core.schemas import Citation


def citations_from_documents(documents: list[Document]) -> list[Citation]:
    seen: set[tuple] = set()
    citations: list[Citation] = []
    for doc in documents:
        metadata = doc.metadata
        key = (
            metadata.get("source_file"),
            metadata.get("page_number"),
            metadata.get("chunk_id"),
        )
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            Citation(
                source_file=metadata.get("source_file", "unknown"),
                page_number=metadata.get("page_number"),
                policy_name=metadata.get("policy_name"),
                section_title=metadata.get("section_title"),
                chunk_id=metadata.get("chunk_id"),
            )
        )
    return citations


def documents_to_context(documents: list[Document]) -> list[dict]:
    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
        }
        for doc in documents
    ]
