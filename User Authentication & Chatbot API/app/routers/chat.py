

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import Conversation, User
from app.schemas import ConversationCreate, ConversationResponse
from app.utils.token import get_current_user
from app.services.chatbot import get_ai_response
import random

router = APIRouter(prefix="/chat", tags=["Chatbot"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ConversationResponse)
def chat(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_msg = data.query
    bot_id = data.bot_id

    if bot_id == 0:
        new_bot_id = random.randint(100000000000000, 999999999999999)
        bot_name = user_msg[:50] if len(user_msg) <= 50 else user_msg[:47] + "..."
        reply = "Hi, how can I help you?"
    else:
        new_bot_id = None
        bot_name = None
        reply = get_ai_response(user_msg)
        
        # Get existing bot_name
        existing = db.query(Conversation).filter(
            Conversation.bot_id == bot_id
        ).first()
        if existing and existing.bot_name:
            bot_name = existing.bot_name

    conversation = Conversation(
        user_id=current_user.id,
        bot_id=bot_id if bot_id != 0 else new_bot_id,
        bot_name=bot_name,
        user_message=user_msg,
        bot_response=reply
    )

    db.add(conversation)
    db.commit()

    return {
        "response": reply,
        "bot_id": new_bot_id,
        "bot_name": bot_name,
        "user_id": current_user.id
    }

@router.get("/history", response_model=List[ConversationResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.asc()).all()

    return [
        {
            "response": c.bot_response,
            "user_message": c.user_message,
            "bot_id": c.bot_id,
            "bot_name": c.bot_name,
            "user_id": c.user_id,
            "created_at": str(c.created_at)
        }
        for c in conversations
    ]