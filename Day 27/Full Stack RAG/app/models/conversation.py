from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )