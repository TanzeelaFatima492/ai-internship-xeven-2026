from fastapi import FastAPI, Request, HTTPException
from collections import defaultdict
import time
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.routers import document_router
from app.api import rag, analytics, auth, document

from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant RAG API")

# CORS FIRST - before any middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter AFTER CORS
rate_store = defaultdict(list)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host
    now = time.time()
    rate_store[ip] = [t for t in rate_store[ip] if now - t < 86400]
   
    if len(rate_store[ip]) >= 30:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Try again later."})
     
    rate_store[ip].append(now)
    response = await call_next(request)
    return response

app.include_router(document_router.router)
app.include_router(rag.router)
app.include_router(analytics.router)
app.include_router(auth.router)
app.include_router(document.router)

@app.get("/")
def home():
    return {"message": "API Running Successfully"}