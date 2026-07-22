from fastapi import FastAPI
from app.api.content import router as content_router

app = FastAPI(title="Multi-Agent Content Studio", version="1.0.0")

app.include_router(content_router, prefix="/api", tags=["Content"])

@app.get("/")
async def root():
    return {
        "message": "Multi-Agent Content Studio is running!",
        "docs": "/docs"
    }

@app.on_event("startup")
async def init_agents():
    print("🤖 Initializing Multi-Agent System...")
    print("✅ Multi-Agent System Ready!")