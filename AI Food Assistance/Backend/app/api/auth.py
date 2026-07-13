from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, Token
from app.auth.auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username exists")
    
    new_user = User(
    username=user.username,
    email=user.email,
    hashed_password=hash_password(user.password),
    role="customer"  # Always customer
)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token({"sub": db_user.username, "role": db_user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role
    }