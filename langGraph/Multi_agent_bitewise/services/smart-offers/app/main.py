from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uvicorn
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="BiteWise Smart Offers Service",
    version="1.0.0",
    description="Generates personalized offers for users"
)

# Configuration
PATTERN_SERVICE_URL = os.getenv("PATTERN_SERVICE_URL", "http://localhost:8001")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8003")

# ==================== OFFER GENERATION ====================

def generate_routine_reminder(profile: Dict) -> Optional[Dict]:
    """Generate routine reminder offer"""
    routine = profile.get("routine", {})
    if routine.get("routine") in ["consistent", "semi_consistent"]:
        usual_time = routine.get("usual_time")
        if usual_time:
            return {
                "type": "routine_reminder",
                "message": f"⏰ Ready to order your usual meal at {usual_time}?",
                "priority": "high",
                "discount": "Free delivery on your usual order"
            }
    return None

def generate_streak_protection(profile: Dict) -> Optional[Dict]:
    """Generate streak protection offer"""
    streak = profile.get("streak", 0)
    if streak >= 3:
        return {
            "type": "streak_protection",
            "message": f"🔥 Don't break your {streak}-day streak! Order now!",
            "priority": "high",
            "discount": "15% off your order"
        }
    return None

def generate_re_engagement(profile: Dict) -> Optional[Dict]:
    """Generate re-engagement offer for inactive users"""
    last_order = profile.get("last_order")
    if last_order:
        try:
            last_order_date = datetime.fromisoformat(last_order)
            days_since = (datetime.now() - last_order_date).days
            if days_since >= 7:
                return {
                    "type": "re_engagement",
                    "message": f"👋 We miss you! It's been {days_since} days. Come back!",
                    "priority": "high",
                    "discount": "25% off your next order"
                }
        except:
            pass
    return None

def generate_combo_deal(profile: Dict) -> Optional[Dict]:
    """Generate combo deal based on frequently paired items"""
    combos = profile.get("preferences", {}).get("combos", [])
    if combos:
        top_combo = combos[0]
        items = top_combo.get("items", [])
        if items and len(items) >= 2:
            return {
                "type": "combo_deal",
                "message": f"🍔 Combo Deal: {items[0]} + {items[1]} - Save 15%!",
                "priority": "medium",
                "discount": "15% off combo"
            }
    return None

def generate_milestone_reward(profile: Dict) -> Optional[Dict]:
    """Generate milestone reward based on total orders"""
    total_orders = profile.get("total_orders", 0)
    
    # Check if user reached a milestone
    milestones = [5, 10, 25, 50, 100]
    for milestone in milestones:
        if total_orders == milestone:
            return {
                "type": "milestone_reward",
                "message": f"🎉 Congratulations! You've placed {milestone} orders!",
                "priority": "high",
                "discount": "Free dessert on your next order"
            }
        elif total_orders > 0 and total_orders % 5 == 0:
            return {
                "type": "milestone_reward",
                "message": f"🎉 You're on a roll! {total_orders} orders and counting!",
                "priority": "medium",
                "discount": "10% off your next order"
            }
    return None

# ==================== MAIN OFFER GENERATOR ====================

def generate_offers(profile: Dict) -> List[Dict]:
    """Generate all possible offers for a user"""
    offers = []
    
    offer_functions = [
        generate_routine_reminder,
        generate_streak_protection,
        generate_re_engagement,
        generate_combo_deal,
        generate_milestone_reward
    ]
    
    for func in offer_functions:
        offer = func(profile)
        if offer:
            offers.append(offer)
    
    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    offers.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 2))
    
    return offers

# ==================== SEND NOTIFICATION WITH RETRY ====================

def send_notification_with_retry(user_id: str, offer: Dict, max_retries: int = 3) -> bool:
    """Send notification with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{NOTIFICATION_SERVICE_URL}/notify",
                json={
                    "user_id": user_id,
                    "offer": offer,
                    "channels": ["in_app", "push"]
                },
                timeout=5
            )
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return False
    return False

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "service": "Smart Offers Service",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/offers/generate/{user_id}")
async def generate_user_offers(user_id: str):
    """Generate personalized offers for a user with notifications"""
    try:
        # Fetch user profile from Pattern Detection Service
        response = requests.get(f"{PATTERN_SERVICE_URL}/user/{user_id}/patterns")
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found or insufficient data")
        
        profile = response.json()
        
        # Check if we have enough data
        if profile.get("status") == "insufficient_data":
            return {
                "user_id": user_id,
                "status": "insufficient_data",
                "message": profile.get("message"),
                "offers": []
            }
        
        # Generate offers
        offers = generate_offers(profile)
        
        # Send notifications for high and medium priority offers
        notifications_sent = 0
        notification_results = []
        
        for offer in offers:
            if offer.get("priority") in ["high", "medium"]:
                # Send notification with retry
                success = send_notification_with_retry(user_id, offer)
                notification_results.append({
                    "offer_type": offer.get("type"),
                    "success": success
                })
                if success:
                    notifications_sent += 1
        
        return {
            "user_id": user_id,
            "total_offers": len(offers),
            "offers": offers,
            "notifications_sent": notifications_sent,
            "notification_results": notification_results
        }
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Pattern Detection Service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/offers/generate/test/{user_id}")
async def test_offers(user_id: str):
    """Test offer generation without sending notifications"""
    try:
        response = requests.get(f"{PATTERN_SERVICE_URL}/user/{user_id}/patterns")
        
        if response.status_code != 200:
            return {
                "user_id": user_id,
                "status": "error",
                "message": "User not found or insufficient data"
            }
        
        profile = response.json()
        
        if profile.get("status") == "insufficient_data":
            return {
                "user_id": user_id,
                "status": "insufficient_data",
                "message": profile.get("message"),
                "offers": []
            }
        
        offers = generate_offers(profile)
        
        return {
            "user_id": user_id,
            "total_offers": len(offers),
            "offers": offers,
            "profile_summary": {
                "total_orders": profile.get("total_orders", 0),
                "streak": profile.get("streak", 0),
                "routine": profile.get("routine", {}).get("routine", "unknown"),
                "favorites": profile.get("preferences", {}).get("favorites", [])[:3]
            }
        }
        
    except requests.exceptions.ConnectionError:
        return {
            "user_id": user_id,
            "status": "error",
            "message": "Pattern Detection Service unavailable at " + PATTERN_SERVICE_URL
        }
    except Exception as e:
        return {
            "user_id": user_id,
            "status": "error",
            "message": str(e)
        }

# ==================== MAIN ====================

if __name__ == "__main__":
    port = int(os.getenv("SMART_OFFERS_SERVICE_PORT", 8002))
    uvicorn.run(app, host="127.0.0.1", port=port)