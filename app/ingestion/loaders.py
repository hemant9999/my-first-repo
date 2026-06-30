from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(path: Path) -> list[Document]:
    loader = PyPDFLoader(str(path))
    docs = loader.load()
    for page_index, doc in enumerate(docs, start=1):
        doc.metadata.update(
            {
                "source_file": path.name,
                "source_path": str(path.resolve()),
                "page_number": doc.metadata.get("page", page_index - 1) + 1,
                "policy_name": path.stem.replace("_", " ").replace("-", " ").title(),
            }
        )
    return docs


def discover_pdfs(path: Path, glob: str = "*.pdf") -> list[Path]:
    if path.is_file() and path.suffix.lower() == ".pdf":
        return [path]
    return sorted(p for p in path.glob(glob) if p.is_file() and p.suffix.lower() == ".pdf")
