import typer
from rich.console import Console
from rich.markdown import Markdown

from app.chatbot.chain import answer_question
from app.core.logging import configure_logging

app = typer.Typer(help="Chat with the policy RAG assistant from the terminal.")
console = Console()


@app.command()
def main() -> None:
    configure_logging()
    console.print("[bold]Policy RAG Assistant[/bold]")
    console.print("Type 'exit' to quit.")
    while True:
        question = console.input("\n[cyan]Question>[/cyan] ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        response = answer_question(question)
        console.print(Markdown(response.answer))
        if response.citations:
            console.print("\n[bold]Citations[/bold]")
            for citation in response.citations:
                page = f", page {citation.page_number}" if citation.page_number else ""
                console.print(f"- {citation.policy_name or citation.source_file}{page}")


if __name__ == "__main__":
    app()
