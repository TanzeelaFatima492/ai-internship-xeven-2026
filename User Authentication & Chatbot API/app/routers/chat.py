from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import Conversation, User
from app.schemas import ConversationCreate, ConversationResponse
from app.utils.token import get_current_user
import uuid

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
    
    # Pehli call → naya bot_id generate karo
    if not bot_id:
        new_bot_id = str(uuid.uuid4()).replace("-", "")[:20]  # "389982399239323"
        reply = "Hi, how can I help you?"
    else:
        # Existing conversation → bot_id null return karo
        new_bot_id = None
        reply = f"Echo: {user_msg}"
    
    conversation = Conversation(
        user_id=current_user.id,
        bot_id=bot_id if bot_id else new_bot_id,
        user_message=user_msg,
        bot_response=reply
    )
    
    db.add(conversation)
    db.commit()
    
    return {
        "response": reply,
        "bot_id": new_bot_id,
        "user_id": current_user.id
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
            "response": c.bot_response,
            "bot_id": c.bot_id,
            "user_id": c.user_id
        }
        for c in conversations
    ]