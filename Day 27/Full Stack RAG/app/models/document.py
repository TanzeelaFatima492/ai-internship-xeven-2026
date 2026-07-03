from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.database.database import Base
from sqlalchemy.orm import relationship


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    filename = Column(String(255), nullable=False, unique=True)

    file_type = Column(String(50), nullable=False)

    file_size = Column(Integer, nullable=False)

    version = Column(Integer, default=1)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    chunks = relationship(
    "Chunk",
    back_populates="document",
    cascade="all, delete"
    )