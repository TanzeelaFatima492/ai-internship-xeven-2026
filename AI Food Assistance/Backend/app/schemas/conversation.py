from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ConversationCreate(BaseModel):
    thread_id: str
    question: str
    answer: str
    sources: Optional[str] = None

class ConversationResponse(BaseModel):
    id: int
    thread_id: str
    question: str
    answer: str
    sources: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ThreadResponse(BaseModel):
    thread_id: str
    messages: List[ConversationResponse]
    created_at: datetime