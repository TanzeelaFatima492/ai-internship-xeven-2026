from fastapi import FastAPI
from app.database.database import Base
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant RAG API"
)


@app.get("/")
def home():
    return {
        "message": "API Running Successfully"
    }