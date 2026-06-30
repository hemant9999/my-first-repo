from dataclasses import asdict, dataclass

from langchain_core.documents import Document

from app.retrieval.retriever import build_retriever
from app.validation.datasets import ExpectedSource, GoldenQuestion


@dataclass
class RetrievalEvalResult:
    id: str
    question: str
    source_hit: bool
    page_hit: bool
    rank: int | None
    expected_sources: list[dict]
    retrieved_context: list[dict]


def _expected_source_dicts(expected_sources: list[ExpectedSource]) -> list[dict]:
    return [source.model_dump() for source in expected_sources]


def _retrieved_context(documents: list[Document]) -> list[dict]:
    context = []
    for rank, doc in enumerate(documents, start=1):
        context.append(
            {
                "rank": rank,
                "source_file": doc.metadata.get("source_file", ""),
                "page_number": doc.metadata.get("page_number"),
                "chunk_id": doc.metadata.get("chunk_id"),
            }
        )
    return context


def _matches_expected(document: Document, expected: ExpectedSource) -> bool:
    if document.metadata.get("source_file") != expected.file:
        return False
    if not expected.pages:
        return True
    return document.metadata.get("page_number") in expected.pages


def evaluate_retrieval_case(case: GoldenQuestion, top_k: int | None = None) -> RetrievalEvalResult:
    retriever = build_retriever(top_k=top_k)
    documents = retriever.invoke(case.question)

    rank = None
    source_hit = False
    page_hit = False
    for index, document in enumerate(documents, start=1):
        if any(
            document.metadata.get("source_file") == source.file
            for source in case.expected_sources
        ):
            source_hit = True
        if any(_matches_expected(document, source) for source in case.expected_sources):
            page_hit = True
            rank = index
            break

    return RetrievalEvalResult(
        id=case.id,
        question=case.question,
        source_hit=source_hit,
        page_hit=page_hit,
        rank=rank,
        expected_sources=_expected_source_dicts(case.expected_sources),
        retrieved_context=_retrieved_context(documents),
    )


def evaluate_retrieval(cases: list[GoldenQuestion], top_k: int | None = None) -> dict:
    results = [evaluate_retrieval_case(case, top_k=top_k) for case in cases]
    total = len(results)
    source_hits = sum(1 for result in results if result.source_hit)
    page_hits = sum(1 for result in results if result.page_hit)
    reciprocal_ranks = [1 / result.rank for result in results if result.rank]
    return {
        "total": total,
        "source_hits": source_hits,
        "page_hits": page_hits,
        "source_recall_at_k": source_hits / total if total else 0,
        "page_recall_at_k": page_hits / total if total else 0,
        "mrr": sum(reciprocal_ranks) / total if total else 0,
        "results": [asdict(result) for result in results],
    }
