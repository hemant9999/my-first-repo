from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ExpectedSource(BaseModel):
    file: str
    pages: list[int] = Field(default_factory=list)


class GoldenQuestion(BaseModel):
    id: str
    question: str
    expected_answer_contains: list[str] = Field(default_factory=list)
    expected_sources: list[ExpectedSource] = Field(default_factory=list)


def load_golden_questions(path: Path) -> list[GoldenQuestion]:
    with path.open("r", encoding="utf-8") as handle:
        raw: list[dict[str, Any]] = yaml.safe_load(handle) or []
    return [GoldenQuestion.model_validate(item) for item in raw]
