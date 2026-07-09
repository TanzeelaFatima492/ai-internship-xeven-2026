from fastapi import FastAPI, Request, HTTPException
from collections import defaultdict
import time

from app.database.database import Base, engine
from app.routers import document_router
from app.api import rag, analytics, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant RAG API")

# Rate limiter
rate_store = defaultdict(list)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host
    now = time.time()
    rate_store[ip] = [t for t in rate_store[ip] if now - t < 60]
    
    if len(rate_store[ip]) >= 10:
        return HTTPException(status_code=429, detail="Rate limit exceeded")
    
    rate_store[ip].append(now)
    response = await call_next(request)
    return response

app.include_router(document_router.router)
app.include_router(rag.router)
app.include_router(analytics.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "API Running Successfully"}