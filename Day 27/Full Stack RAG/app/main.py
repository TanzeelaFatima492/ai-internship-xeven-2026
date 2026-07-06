from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine

import app.models

from app.routers import document_router
from app.api import rag  # ✅ NEW: Import RAG router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant RAG API"
)

app.include_router(
    document_router.router
)

app.include_router(
    rag.router  # ✅ NEW: Register RAG endpoints
)

@app.get("/")
def home():
    return {
        "message": "API Running Successfully"
    }