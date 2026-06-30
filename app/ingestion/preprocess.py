import re

from langchain_core.documents import Document

_WHITESPACE_RE = re.compile(r"[ \t]+")
_NEWLINE_RE = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = _WHITESPACE_RE.sub(" ", text)
    text = _NEWLINE_RE.sub("\n\n", text)
    return text.strip()


def clean_documents(documents: list[Document]) -> list[Document]:
    cleaned: list[Document] = []
    for doc in documents:
        text = clean_text(doc.page_content)
        if text:
            cleaned.append(Document(page_content=text, metadata=dict(doc.metadata)))
    return cleaned
