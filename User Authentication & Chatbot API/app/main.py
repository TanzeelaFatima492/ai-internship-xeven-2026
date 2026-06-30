from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Authentication & Chatbot API",
    version="1.0.0"
)

# Register Routers
app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "message": "User Authentication & Chatbot API is Running"
    }