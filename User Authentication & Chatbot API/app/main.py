from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Authentication API")

app.include_router(auth.router)


@app.get("/")
def home():
    return {"message": "API is running"}