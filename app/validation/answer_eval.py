import re
from dataclasses import asdict, dataclass

from app.chatbot.chain import answer_question
from app.validation.datasets import GoldenQuestion

_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


@dataclass
class AnswerEvalResult:
    id: str
    question: str
    contains_expected_terms: bool
    has_citations: bool
    citation_source_hit: bool
    citation_page_hit: bool
    passed: bool
    answer: str


def _normalize_text(value: str) -> str:
    return _NON_ALNUM_RE.sub("", value.lower())


def _contains_expected_terms(answer: str, expected_terms: list[str]) -> bool:
    normalized_answer = _normalize_text(answer)
    return all(_normalize_text(term) in normalized_answer for term in expected_terms)


def _citation_source_hit(case: GoldenQuestion, response) -> bool:
    if not case.expected_sources:
        return True
    expected_files = {source.file for source in case.expected_sources}
    return any(citation.source_file in expected_files for citation in response.citations)


def _citation_page_hit(case: GoldenQuestion, response) -> bool:
    if not case.expected_sources:
        return True
    for expected in case.expected_sources:
        if not expected.pages:
            continue
        for citation in response.citations:
            if citation.source_file == expected.file and citation.page_number in expected.pages:
                return True
    return not any(source.pages for source in case.expected_sources)


def evaluate_answer_case(case: GoldenQuestion) -> AnswerEvalResult:
    response = answer_question(case.question)
    contains_expected_terms = _contains_expected_terms(
        response.answer,
        case.expected_answer_contains,
    )
    has_citations = bool(response.citations)
    citation_source_hit = _citation_source_hit(case, response)
    citation_page_hit = _citation_page_hit(case, response)
    passed = contains_expected_terms and has_citations and citation_source_hit and citation_page_hit
    return AnswerEvalResult(
        id=case.id,
        question=case.question,
        contains_expected_terms=contains_expected_terms,
        has_citations=has_citations,
        citation_source_hit=citation_source_hit,
        citation_page_hit=citation_page_hit,
        passed=passed,
        answer=response.answer,
    )


def evaluate_answers(cases: list[GoldenQuestion]) -> dict:
    results = [evaluate_answer_case(case) for case in cases]
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    return {
        "total": total,
        "passed": passed,
        "pass_rate": passed / total if total else 0,
        "results": [asdict(result) for result in results],
    }
