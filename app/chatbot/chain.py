from langchain_google_vertexai import ChatVertexAI

from app.chatbot.prompts import RAG_PROMPT
from app.core.config import Settings, get_settings
from app.core.schemas import ChatResponse
from app.retrieval.citations import citations_from_documents, documents_to_context
from app.retrieval.retriever import build_retriever


def build_llm(settings: Settings | None = None) -> ChatVertexAI:
    settings = settings or get_settings()
    kwargs = {
        "model": settings.gemini_model,
        "location": settings.google_cloud_location,
        "temperature": 0,
    }
    if settings.google_cloud_project:
        kwargs["project"] = settings.google_cloud_project
    return ChatVertexAI(**kwargs)


def format_context(documents) -> str:
    blocks: list[str] = []
    for i, doc in enumerate(documents, start=1):
        metadata = doc.metadata
        source = metadata.get("source_file", "unknown")
        page = metadata.get("page_number", "unknown")
        policy = metadata.get("policy_name", source)
        blocks.append(
            f"[{i}] Policy: {policy}\nSource: {source}\nPage: {page}\nText:\n{doc.page_content}"
        )
    return "\n\n".join(blocks)


def answer_question(
    question: str,
    top_k: int | None = None,
    metadata_filter: dict | None = None,
    settings: Settings | None = None,
) -> ChatResponse:
    settings = settings or get_settings()
    retriever = build_retriever(settings, top_k=top_k, metadata_filter=metadata_filter)
    documents = retriever.invoke(question)

    if not documents:
        return ChatResponse(
            answer="The policy documents do not contain enough information to answer that.",
            citations=[],
            retrieved_context=[],
        )

    llm = build_llm(settings)
    prompt_value = RAG_PROMPT.invoke(
        {
            "question": question,
            "context": format_context(documents),
        }
    )
    response = llm.invoke(prompt_value)
    return ChatResponse(
        answer=response.content,
        citations=citations_from_documents(documents),
        retrieved_context=documents_to_context(documents),
    )
