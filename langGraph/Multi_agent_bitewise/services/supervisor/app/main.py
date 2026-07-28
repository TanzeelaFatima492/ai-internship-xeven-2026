from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from .agent import get_supervisor

load_dotenv()

app = FastAPI(
    title="BiteWise Supervisor Agent",
    version="1.0.0",
    description="Orchestrates all BiteWise agents"
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================
class SupervisorRequest(BaseModel):
    user_id: str
    query: str
    thread_id: Optional[str] = None

# ==================== ENDPOINTS ====================

@app.post("/agent/supervisor")
async def supervisor_endpoint(request: SupervisorRequest):
    """Orchestrate all agents"""
    try:
        agent = get_supervisor()
        result = await agent.run(request.user_id, request.query, request.thread_id)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {
        "service": "Supervisor Agent",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.getenv("SUPERVISOR_PORT", 8004))
    uvicorn.run(app, host="127.0.0.1", port=port)