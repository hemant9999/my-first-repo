from app.validation.datasets import ExpectedSource, GoldenQuestion
from app.validation.retrieval_eval import RetrievalEvalResult


def test_retrieval_eval_result_shape() -> None:
    case = GoldenQuestion(
        id="case_1",
        question="What is covered?",
        expected_sources=[ExpectedSource(file="policy.pdf", pages=[1])],
    )
    result = RetrievalEvalResult(
        id=case.id,
        question=case.question,
        source_hit=True,
        page_hit=True,
        rank=1,
        expected_sources=[{"file": "policy.pdf", "pages": [1]}],
        retrieved_context=[{"rank": 1, "source_file": "policy.pdf", "page_number": 1}],
    )
    assert result.source_hit is True
    assert result.page_hit is True
    assert result.rank == 1
