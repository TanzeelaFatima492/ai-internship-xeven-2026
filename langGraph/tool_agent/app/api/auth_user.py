from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.schema.schemas import UserProfileSchema, UserLogin
from app.db.operation import signup_service, login_service

auth_router = APIRouter()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserProfileSchema, db: AsyncSession = Depends(get_async_session)):
    """Create a new user account."""
    return await signup_service(user, db)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_session)):
    """Authenticate user and return JWT token."""
    return await login_service(user, db)
        