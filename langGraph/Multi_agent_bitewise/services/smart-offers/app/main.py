from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os
import json
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List

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

@app.post("/offers/generate/{user_id}")
async def generate_offers(user_id: str):
    """Generate personalized offers for a user"""
    try:
        # Call pattern detection service to get user patterns
        pattern_response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        
        if pattern_response.status_code != 200:
            return {"status": "insufficient_data", "message": "Could not fetch user patterns", "offers": [], "total_offers": 0}
        
        profile = pattern_response.json()
        
        if profile.get("status") == "insufficient_data":
            return {"status": "insufficient_data", "message": profile.get("message", "Insufficient data"), "offers": [], "total_offers": 0}
        
        # Generate offers based on patterns
        offers = []
        total_orders = profile.get("total_orders", 0)
        streak = profile.get("streak", 0)
        routine = profile.get("routine", {})
        preferences = profile.get("preferences", {})
        spending = profile.get("spending", {})
        timing = profile.get("timing_pattern", {})
        
        # Routine reminder offer
        if routine.get("routine") in ["consistent", "semi_consistent"]:
            offers.append({
                "type": "routine_reminder",
                "message": f"⏰ Ready to order your usual meal at {routine.get('usual_time', '14:00')}?",
                "priority": "high",
                "discount": "Free delivery"
            })
        
        # Streak protection offer
        if streak >= 3:
            offers.append({
                "type": "streak_protection",
                "message": f"🔥 Don't break your {streak}-day streak! Order now!",
                "priority": "high",
                "discount": "15% off your order"
            })
        
        # Combo deal based on preferences
        combos = preferences.get("combos", [])
        if combos and len(combos) > 0:
            top_combo = combos[0]
            items = top_combo.get("items", [])
            if len(items) >= 2:
                offers.append({
                    "type": "combo_deal",
                    "message": f"🍔 Combo: {items[0]} + {items[1]} - Save 15%!",
                    "priority": "medium",
                    "discount": "15% off combo"
                })
        
        # Milestone reward
        milestones = [5, 10, 25, 50, 100]
        milestone_matched = None
        for m in milestones:
            if total_orders == m:
                milestone_matched = m
                break
        if milestone_matched:
            offers.append({
                "type": "milestone_reward",
                "message": f"🎉 {milestone_matched} orders! You've earned a reward!",
                "priority": "high",
                "discount": "Free dessert"
            })
        elif total_orders > 0 and total_orders % 5 == 0:
            offers.append({
                "type": "milestone_reward",
                "message": f"🎉 {total_orders} orders and counting!",
                "priority": "medium",
                "discount": "10% off"
            })
        
        # Re-engagement for inactive users
        last_order = profile.get("last_order")
        if last_order:
            from datetime import datetime as dt
            try:
                last_date = dt.fromisoformat(last_order)
                days_since = (dt.now() - last_date).days
                if days_since >= 7:
                    offers.append({
                        "type": "re_engagement",
                        "message": f"👋 We miss you! It's been {days_since} days!",
                        "priority": "high",
                        "discount": "25% off your next order"
                    })
            except:
                pass
        
        # Send notifications for high priority offers
        for offer in offers:
            if offer.get("priority") == "high":
                try:
                    requests.post(
                        "http://localhost:8003/notify",
                        json={
                            "user_id": user_id,
                            "message": offer.get("message", ""),
                            "type": "offer",
                            "offer": offer
                        }
                    )
                except:
                    pass
        
        # If no offers generated, create a default welcome offer
        if len(offers) == 0:
            offers.append({
                "type": "welcome_offer",
                "message": "🎉 Welcome! Enjoy a special discount on your next order!",
                "priority": "medium",
                "discount": "10% off"
            })
        
        return {
            "user_id": user_id,
            "total_offers": len(offers),
            "offers": offers,
            "generated_at": datetime.now().isoformat()
        }
        
    except requests.exceptions.ConnectionError:
        # If pattern service is down, return mock offers
        mock_offers = [
            {"type": "welcome_offer", "message": "🎉 Welcome! Enjoy 10% off your first order!", "priority": "high", "discount": "10% off"},
            {"type": "combo_deal", "message": "🍔 Burger + Fries Combo - Save 15%!", "priority": "medium", "discount": "15% off combo"},
            {"type": "free_delivery", "message": "🚚 Free delivery on orders above $20!", "priority": "low", "discount": "Free delivery"}
        ]
        return {"user_id": user_id, "total_offers": len(mock_offers), "offers": mock_offers, "generated_at": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/offers/user/{user_id}/latest")
async def get_latest_offer(user_id: str):
    """Get the latest offer for a user"""
    return {"offer": {"type": "welcome_offer", "message": "🎉 Check your personalized offers!", "priority": "medium", "discount": "10% off"}}

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
