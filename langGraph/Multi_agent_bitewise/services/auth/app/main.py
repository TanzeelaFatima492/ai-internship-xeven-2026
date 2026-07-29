from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.database.models import User
from shared.database.database import get_db, engine, Base

load_dotenv()

# ==================== CONFIG ====================
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

# ==================== PASSWORD CONTEXT ====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==================== APP ====================
app = FastAPI(
    title="BiteWise Auth Service",
    version="1.0.0",
    description="Authentication Service with JWT"
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    token: Optional[str] = None

# ==================== HELPERS ====================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(user_id: str, email: str) -> str:
    return jwt.encode(
        {"user_id": str(user_id), "email": email, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# ==================== ENDPOINTS ====================

@app.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = hash_password(request.password)
    user = User(
        name=request.name,
        email=request.email,
        phone=request.phone,
        password_hash=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_token(user.id, user.email)
    
    return AuthResponse(
        success=True,
        message="User registered successfully",
        user_id=str(user.id),
        name=user.name,
        email=user.email,
        token=token
    )

@app.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login and get JWT token"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user.id, user.email)
    
    return AuthResponse(
        success=True,
        message="Login successful",
        user_id=str(user.id),
        name=user.name,
        email=user.email,
        token=token
    )

@app.get("/verify")
async def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "success": True,
            "valid": True,
            "user_id": payload.get("user_id"),
            "email": payload.get("email")
        }
    except JWTError:
        return {"success": False, "valid": False, "error": "Invalid token"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"service": "Auth Service", "status": "running"}

if __name__ == "__main__":
    port = int(os.getenv("AUTH_SERVICE_PORT", 8005))
    uvicorn.run(app, host="127.0.0.1", port=port)