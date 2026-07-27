from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict, Optional
import uvicorn
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="BiteWise Notification Service",
    version="1.0.0",
    description="Sends real-time notifications using LangGraph Agent"
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
class NotificationRequest(BaseModel):
    user_id: str
    query: str
    thread_id: Optional[str] = None

# ==================== AGENT ENDPOINTS ====================

@app.post("/agent/notify")
async def agent_notify(request: NotificationRequest):
    """Use LangGraph agent to handle notification queries"""
    try:
        # ✅ Sahi import
        from agent import get_notification_agent
        agent = get_notification_agent()
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
        "service": "Notification Service",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "agent": "LangGraph enabled"
    }

# ==================== MAIN ====================

if __name__ == "__main__":
    port = int(os.getenv("NOTIFICATION_SERVICE_PORT", 8003))
    uvicorn.run(app, host="127.0.0.1", port=port)