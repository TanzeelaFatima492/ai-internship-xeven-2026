from sqlalchemy import Column, Integer, Text, DateTime, String
from sqlalchemy.sql import func

from app.database.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, nullable=False, index=True)  # ✅ Thread grouping
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text, nullable=True)  # JSON stored as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())