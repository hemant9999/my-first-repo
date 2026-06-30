from pathlib import Path
from typing import Literal

import typer
from rich.console import Console

from app.core.logging import configure_logging
from app.validation.answer_eval import evaluate_answers
from app.validation.datasets import load_golden_questions
from app.validation.reports import write_json_report
from app.validation.retrieval_eval import evaluate_retrieval

app = typer.Typer(help="Validate RAG retrieval and answer quality.")
console = Console()
DATASET_ARGUMENT = typer.Argument(Path("data/eval/pearl_stay_guest_guide.yaml"))
MODE_OPTION = typer.Option("retrieval")
OUTPUT_DIR_OPTION = typer.Option(Path("data/eval/reports"))
TOP_K_OPTION = typer.Option(None, help="Override retriever top_k for retrieval validation.")


@app.command()
def main(
    dataset: Path = DATASET_ARGUMENT,
    mode: Literal["retrieval", "answer", "all"] = MODE_OPTION,
    output_dir: Path = OUTPUT_DIR_OPTION,
    top_k: int | None = TOP_K_OPTION,
) -> None:
    configure_logging()
    cases = load_golden_questions(dataset)
    if mode in {"retrieval", "all"}:
        retrieval_report = evaluate_retrieval(cases, top_k=top_k)
        path = write_json_report(retrieval_report, output_dir, "retrieval")
        console.print(
            "[green]Retrieval[/green] "
            f"source_recall@k={retrieval_report['source_recall_at_k']:.2f}, "
            f"page_recall@k={retrieval_report['page_recall_at_k']:.2f}, "
            f"MRR={retrieval_report['mrr']:.2f}; report={path}"
        )
    if mode in {"answer", "all"}:
        answer_report = evaluate_answers(cases)
        path = write_json_report(answer_report, output_dir, "answer")
        console.print(
            f"[green]Answers[/green] pass_rate={answer_report['pass_rate']:.2f}; report={path}"
        )


if __name__ == "__main__":
    app()
