from pathlib import Path

import typer
from rich.console import Console

from app.core.logging import configure_logging
from app.ingestion.pipeline import ingest_path

app = typer.Typer(help="Ingest policy PDFs into local Chroma.")
console = Console()
PATH_ARGUMENT = typer.Argument(default=None, help="PDF file or directory to ingest.")
GLOB_OPTION = typer.Option("*.pdf", help="Glob used when path is a directory.")


@app.command()
def main(
    path: Path | None = PATH_ARGUMENT,
    glob: str = GLOB_OPTION,
) -> None:
    configure_logging()
    results = ingest_path(path=path, glob=glob)
    total_chunks = sum(result.chunks for result in results)
    for result in results:
        message = (
            f"[green]Indexed[/green] {result.source_file}: "
            f"{result.pages} pages, {result.chunks} chunks"
        )
        console.print(
            message
        )
    console.print(f"[bold]Done.[/bold] {len(results)} documents, {total_chunks} chunks.")


if __name__ == "__main__":
    app()
