from fastapi import APIRouter

from app.chatbot.chain import answer_question
from app.core.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return answer_question(
        question=request.question,
        top_k=request.top_k,
        metadata_filter=request.filter,
    )
