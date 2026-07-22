
import logging
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import UserProfiles
from app.schema.schemas import UserProfileSchema, UserLogin
from app.utils.auth_utils import (
    hash_password,
    validate_email,
    sign_jwt,
    verify_password,
)

logger = logging.getLogger(__name__)



async def signup_service(user: UserProfileSchema, db: AsyncSession) -> dict:
    """Register a new user."""
    # Validate email format
    if not validate_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Check if user already exists
    query = select(UserProfiles).where(UserProfiles.email == user.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create new user
    try:
        hashed_password = hash_password(user.password)
        new_user = UserProfiles(
            email=user.email,
            password=hashed_password,
            user_name=user.user_name,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "data": {
                "user_id": str(new_user.user_id),
                "email": new_user.email,
                "user_name": new_user.user_name,
            },
            "succeeded": True
        }
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error during signup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


async def login_service(user: UserLogin, db: AsyncSession) -> dict:
    """Authenticate user and return JWT token."""
    try:
        # Query user by email
        query = select(UserProfiles).where(UserProfiles.email == user.email)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Generate JWT token
        token_data = sign_jwt(str(db_user.user_id))

        return {
            "message": "Login successful",
            "data": {
                "user_id": str(db_user.user_id),
                "email": db_user.email,
                "user_name": db_user.user_name,
                "access_token": token_data["access_token"],
            },
            "succeeded": True
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )



