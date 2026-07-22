from sqlalchemy import Column, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Uuid
from uuid import uuid4
from app.db.base import BaseDBModel


class UserProfiles(BaseDBModel):
    """User profile model for authentication and user management."""

    user_id = mapped_column(Uuid, primary_key=True, default=uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    user_name = Column(String(100), nullable=False, index=True)