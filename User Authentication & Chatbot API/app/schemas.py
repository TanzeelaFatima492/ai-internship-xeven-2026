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
    message: str

class ConversationResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    user_id: int | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True