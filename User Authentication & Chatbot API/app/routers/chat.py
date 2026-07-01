from fastapi import APIRouter

from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot import chatbot_reply

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chatbot_reply(request.message)
    return ChatResponse(reply=response)