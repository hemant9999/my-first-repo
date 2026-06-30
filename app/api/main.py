from fastapi import FastAPI

from app.api.routes import chat, health, ingest

app = FastAPI(
    title="Policy RAG Assistant",
    version="0.1.0",
    description="LangChain + Vertex AI Gemini + local Chroma policy RAG service.",
)

app.include_router(health.router)
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
