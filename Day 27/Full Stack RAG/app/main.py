from fastapi import FastAPI, Request, HTTPException
from collections import defaultdict
import time

from app.database.database import Base, engine
from app.routers import document_router
from app.api import rag, analytics, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant RAG API")

# Simple rate limiter
rate_limit_store = defaultdict(list)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    # Clean old entries
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if now - t < 60]
    
    # Check limit: 10 requests per minute
    if len(rate_limit_store[client_ip]) >= 10:
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
    
    rate_limit_store[client_ip].append(now)
    return await call_next(request)

app.include_router(document_router.router)
app.include_router(rag.router)
app.include_router(analytics.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "API Running Successfully"}