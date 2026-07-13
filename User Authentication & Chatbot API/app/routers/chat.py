from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Conversation, User
from app.schemas import ConversationCreate, ConversationResponse
from app.utils.token import get_current_user
from app.services.chatbot import get_ai_response
import random

router = APIRouter(prefix="/chat", tags=["Chatbot"])

DAILY_LIMIT = 30  # ✅ 30 messages per day

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_rate_limit(user_id: int, db: Session):
    """Check if user has exceeded daily message limit"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    count = db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.created_at >= today_start
    ).count()
    
    if count >= DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit reached: {DAILY_LIMIT} messages per day. Please try again tomorrow."
        )
    return count

@router.post("/", response_model=ConversationResponse)
def chat(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ Rate limit check
    check_rate_limit(current_user.id, db)
    
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

    # ✅ Remaining messages count
    remaining = DAILY_LIMIT - db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.created_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()

    return {
        "response": reply,
        "bot_id": new_bot_id,
        "bot_name": bot_name,
        "user_id": current_user.id,
        "remaining_messages": remaining  # ✅ Kitne messages bache
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