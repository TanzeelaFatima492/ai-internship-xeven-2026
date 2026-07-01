from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import User, Conversation
from app.routers import auth, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Authentication & Chatbot API")

# CORS - Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "User Authentication & Chatbot API is Running!"}