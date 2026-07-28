from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict, List, Dict, Any
import json
import uuid
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==================== STATE ====================
class AuthState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    email: str
    token: str
    is_authenticated: bool
    last_action: str

# ==================== TOOLS ====================

@tool
def signup(name: str, email: str, password: str, phone: str = "") -> str:
    """
    Register a new user.
    
    Args:
        name: Full name of the user
        email: Email address (unique)
        password: Password (min 8 characters)
        phone: Optional phone number
    
    Returns:
        User details and JWT token
    """
    try:
        # Hash password
        hashed = pwd_context.hash(password)
        
        # Mock user creation - replace with DB
        user_id = str(uuid.uuid4())
        token = jwt.encode(
            {"user_id": user_id, "email": email, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        return json.dumps({
            "success": True,
            "message": "User registered successfully",
            "user_id": user_id,
            "name": name,
            "email": email,
            "token": token
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@tool
def login(email: str, password: str) -> str:
    """
    Login and get JWT token.
    
    Args:
        email: User's email
        password: User's password
    
    Returns:
        JWT token and user details
    """
    try:
        # Mock user validation - replace with DB
        # For demo, accept any email with password length >= 8
        if len(password) < 8:
            return json.dumps({"success": False, "error": "Invalid credentials"})
        
        user_id = str(uuid.uuid4())
        token = jwt.encode(
            {"user_id": user_id, "email": email, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        return json.dumps({
            "success": True,
            "message": "Login successful",
            "user_id": user_id,
            "email": email,
            "token": token
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@tool
def verify_token(token: str) -> str:
    """
    Verify if JWT token is valid.
    
    Args:
        token: JWT token to verify
    
    Returns:
        User details if valid, error if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return json.dumps({
            "success": True,
            "valid": True,
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "expires_at": datetime.fromtimestamp(payload.get("exp")).isoformat()
        })
    except JWTError as e:
        return json.dumps({"success": False, "valid": False, "error": str(e)})


@tool
def logout() -> str:
    """
    Logout user (client-side token removal).
    
    Returns:
        Success message
    """
    return json.dumps({"success": True, "message": "Logout successful"})


@tool
def refresh_token(token: str) -> str:
    """
    Refresh JWT token.
    
    Args:
        token: Existing JWT token
    
    Returns:
        New JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        new_token = jwt.encode(
            {"user_id": payload.get("user_id"), "email": payload.get("email"), "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return json.dumps({
            "success": True,
            "message": "Token refreshed",
            "token": new_token
        })
    except JWTError as e:
        return json.dumps({"success": False, "error": str(e)})


@tool
def get_current_user(token: str) -> str:
    """
    Get current user details from token.
    
    Args:
        token: JWT token
    
    Returns:
        User details
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return json.dumps({
            "success": True,
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "expires_at": datetime.fromtimestamp(payload.get("exp")).isoformat()
        })
    except JWTError as e:
        return json.dumps({"success": False, "error": str(e)})

# ==================== ALL TOOLS ====================
AUTH_TOOLS = [
    signup,
    login,
    verify_token,
    logout,
    refresh_token,
    get_current_user
]

# ==================== AGENT ====================
class AuthAgent:
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        self.llm = ChatOllama(
            model=model,
            temperature=0.3,
            base_url="http://localhost:11434"
        ).bind_tools(AUTH_TOOLS)
        
        self.tool_node = ToolNode(AUTH_TOOLS)
        self.memory = MemorySaver()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        def call_agent(state: AuthState):
            response = self.llm.invoke(state["messages"])
            return {"messages": [response]}
        
        workflow = StateGraph(AuthState)
        workflow.add_node("agent", call_agent)
        workflow.add_node("tools", self.tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {"tools": "tools", END: END}
        )
        workflow.add_edge("tools", "agent")
        
        return workflow.compile(checkpointer=self.memory)
    
    async def run(self, query: str, thread_id: str = None) -> Dict:
        thread_id = thread_id or f"auth-{uuid.uuid4().hex[:8]}"
        config = {"configurable": {"thread_id": thread_id}}
        
        result = await self.graph.ainvoke(
            {
                "messages": [{"role": "user", "content": query}],
                "user_id": "",
                "email": "",
                "token": "",
                "is_authenticated": False,
                "last_action": ""
            },
            config=config
        )
        
        messages = result.get("messages", [])
        final_response = messages[-1].content if messages else "No response"
        
        return {
            "thread_id": thread_id,
            "response": final_response
        }

# ==================== SINGLETON ====================
auth_agent = None

def get_auth_agent():
    global auth_agent
    if auth_agent is None:
        auth_agent = AuthAgent()
    return auth_agent