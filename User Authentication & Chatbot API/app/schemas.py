from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ConversationCreate(BaseModel):
    query: str
    bot_id: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "query": "hi",
                "bot_id": 0
            }
        }

class ConversationResponse(BaseModel):
    response: str
    user_message: str | None = None
    bot_id: int | None = None
    bot_name: str | None = None
    user_id: int | None = None
    created_at: datetime | None = None
    remaining_messages: int | None = None  # ✅ NEW

    class Config:
        from_attributes = True