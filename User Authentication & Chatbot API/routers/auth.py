from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import authenticate_user
from app.database import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
)
from app.utils.hashing import Hash
from app.utils.token import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=Hash.bcrypt(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=Token,
)
def login(user: UserLogin, db: Session = Depends(get_db)):

    authenticated_user = authenticate_user(
        user.email,
        user.password,
        db,
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={
            "sub": authenticated_user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }