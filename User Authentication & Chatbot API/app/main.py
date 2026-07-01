from fastapi import APIRouter

from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot import chatbot_response

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    return chatbot_response(request.message)