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
    bot_id: int                    
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ConversationCreate(BaseModel):
    query: str              
    bot_id: int = 0        

class ConversationResponse(BaseModel):
    response: str 
    bot_id: int | None = None
    user_id: int | None = None
    
    class Config:
        from_attributes = True