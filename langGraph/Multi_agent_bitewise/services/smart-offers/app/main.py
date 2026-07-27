from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

app = FastAPI(
    title="BiteWise Smart Offers Service",
    version="1.0.0",
    description="Generates personalized offers using LangGraph Agent"
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
class OfferRequest(BaseModel):
    user_id: str
    query: str
    thread_id: Optional[str] = None

# ==================== AGENT ENDPOINTS ====================

@app.post("/agent/offers")
async def agent_offers(request: OfferRequest):
    """Use LangGraph agent to handle offer queries"""
    try:
        from agent import get_offer_agent
        agent = get_offer_agent()
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
        "service": "Smart Offers Service",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "agent": "LangGraph enabled"
    }

if __name__ == "__main__":
    port = int(os.getenv("SMART_OFFERS_SERVICE_PORT", 8002))
    uvicorn.run(app, host="127.0.0.1", port=port)