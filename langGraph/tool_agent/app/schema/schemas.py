from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from typing import TypedDict, Optional



class UserProfileSchema(BaseModel):
    """User registration request schema."""
    user_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)


class UserLogin(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str


class ChatRequestAgent(BaseModel):
    """Chat agent request schema."""
    query: str
    bot_id: Optional[str] = None
    index_name: str
    
    
class LanggraphAgentRequest(BaseModel):
    query : str
    bot_id : str
    
    
    
class AgentState(TypedDict):
    user_query: str
    intent: str        
    final_response: str   
    bot_id: Optional[str]    

