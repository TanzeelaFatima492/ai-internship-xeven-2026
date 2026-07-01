from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import Conversation, User
from app.schemas import ConversationCreate, ConversationResponse
from app.utils.token import get_current_user

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
    # Generate bot response
    user_msg = data.message
    reply = f"Hello! You said: {user_msg}"  # ← Always respond
    
    conversation = Conversation(
        user_id=current_user.id,
        user_message=user_msg,
        bot_response=reply
    )
    
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return {
        "id": conversation.id,
        "user_message": conversation.user_message,
        "bot_response": conversation.bot_response,
        "user_id": current_user.id,
        "bot_id": current_user.id,
        "created_at": conversation.created_at
    }

@router.get("/history", response_model=List[ConversationResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.desc()).all()
    
    return [
        {
            "id": c.id,
            "user_message": c.user_message,
            "bot_response": c.bot_response,
            "user_id": current_user.id,
            "bot_id": current_user.id,
            "created_at": c.created_at
        }
        for c in conversations
    ]