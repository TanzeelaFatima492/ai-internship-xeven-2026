from sqlalchemy import Column, Integer, Text, ForeignKey

from app.database.database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    content = Column(Text, nullable=False)