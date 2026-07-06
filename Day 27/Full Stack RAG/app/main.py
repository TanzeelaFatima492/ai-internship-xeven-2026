from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine

import app.models

from app.routers import document_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Restaurant RAG API"
)


app.include_router(
    document_router.router
)


@app.get("/")
def home():

    return {

        "message": "API Running Successfully"

    }