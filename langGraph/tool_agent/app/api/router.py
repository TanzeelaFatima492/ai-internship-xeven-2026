from fastapi import APIRouter
from app.api.auth_user import auth_router
from app.api.chatbot import chatbot_router

api_router = APIRouter()
api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(chatbot_router, tags=["Chatbot"])
