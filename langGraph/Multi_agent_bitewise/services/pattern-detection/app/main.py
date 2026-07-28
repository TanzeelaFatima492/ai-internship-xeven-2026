import sys
import os

# Root folder path
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict, Optional
import uvicorn
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from pydantic import BaseModel

from shared.database.models import User, Order
from shared.database.database import get_db, engine, Base
from auth_agent import get_auth_agent

load_dotenv()

# ==================== CREATE TABLES ====================
Base.metadata.create_all(bind=engine)

# ==================== APP ====================
app = FastAPI(
    title="BiteWise Pattern Detection Service",
    version="1.0.0",
    description="Detects user behavior patterns from order history"
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
class AuthRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None

# ==================== AUTH AGENT ENDPOINTS ====================

@app.post("/agent/auth")
async def agent_auth(request: AuthRequest):
    """Use LangGraph agent for authentication"""
    try:
        agent = get_auth_agent()
        result = await agent.run(request.query, request.thread_id)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== EXISTING ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "service": "Pattern Detection Service",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/user/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user details"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "created_at": user.created_at.isoformat(),
        "total_orders": len(user.orders)
    }

@app.post("/user")
async def create_user(name: str, email: str, phone: str = None, db: Session = Depends(get_db)):
    """Create a new user"""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = User(name=name, email=email, phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "message": "User created successfully",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.post("/user/{user_id}/order")
async def add_order(user_id: str, items: List[Dict], db: Session = Depends(get_db)):
    """Add a new order for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    total = sum(item.get("price", 0) for item in items)
    order = Order(user_id=user_id, items=items, total=total)
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return {
        "message": "Order added successfully",
        "order_id": order.id,
        "total": total,
        "timestamp": order.timestamp.isoformat()
    }

@app.get("/user/{user_id}/orders")
async def get_user_orders(user_id: str, db: Session = Depends(get_db)):
    """Get all orders for a user"""
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    
    return {
        "user_id": user_id,
        "total_orders": len(orders),
        "orders": [
            {
                "id": order.id,
                "items": order.items,
                "total": order.total,
                "status": order.status,
                "timestamp": order.timestamp.isoformat()
            }
            for order in orders
        ]
    }

@app.get("/user/{user_id}/patterns")
async def get_user_patterns(user_id: str, db: Session = Depends(get_db)):
    """Analyze user behavior and return patterns"""
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    
    if len(orders) < 3:
        return {
            "user_id": user_id,
            "status": "insufficient_data",
            "message": "Need at least 3 orders to detect patterns",
            "total_orders": len(orders)
        }
    
    orders_data = [
        {
            "id": order.id,
            "items": order.items,
            "total": order.total,
            "timestamp": order.timestamp
        }
        for order in orders
    ]
    
    routine = detect_order_routine(orders_data)
    preferences = detect_food_preferences(orders_data)
    spending = detect_spending_pattern(orders_data)
    streak = calculate_streak(orders_data)
    timing_pattern = detect_timing_pattern(orders_data)
    
    profile = {
        "user_id": user_id,
        "total_orders": len(orders_data),
        "routine": routine,
        "preferences": preferences,
        "spending": spending,
        "streak": streak,
        "timing_pattern": timing_pattern,
        "last_order": orders_data[-1]["timestamp"].isoformat(),
        "analyzed_at": datetime.now().isoformat()
    }
    
    return profile

# ==================== PATTERN DETECTION FUNCTIONS ====================

def detect_order_routine(orders: List[Dict]) -> Dict:
    if len(orders) < 3:
        return {"routine": "unknown", "confidence": 0.0}
    
    hours = []
    days_of_week = []
    
    for order in orders:
        timestamp = order["timestamp"]
        hours.append(timestamp.hour)
        days_of_week.append(timestamp.weekday())
    
    avg_hour = sum(hours) / len(hours)
    max_hour = max(hours)
    min_hour = min(hours)
    time_variation = max_hour - min_hour
    
    unique_days = len(set(days_of_week))
    day_consistency = unique_days / len(orders)
    
    if time_variation <= 2:
        routine = "consistent"
        confidence = 0.9
    elif time_variation <= 4:
        routine = "semi_consistent"
        confidence = 0.6
    else:
        routine = "irregular"
        confidence = 0.2
    
    return {
        "routine": routine,
        "usual_time": f"{int(avg_hour)}:00" if routine != "irregular" else None,
        "time_variation": round(time_variation, 2),
        "day_consistency": round((1 - day_consistency) * 100, 2),
        "confidence": confidence,
        "orders_analyzed": len(orders)
    }

def detect_food_preferences(orders: List[Dict]) -> Dict:
    all_items = []
    category_count = {}
    item_count = {}
    price_range = []
    
    for order in orders:
        for item in order["items"]:
            name = item["name"]
            category = item.get("category", "unknown")
            price = item.get("price", 0)
            
            all_items.append(name)
            item_count[name] = item_count.get(name, 0) + 1
            category_count[category] = category_count.get(category, 0) + 1
            price_range.append(price)
    
    favorites = sorted(item_count.items(), key=lambda x: x[1], reverse=True)[:5]
    favorite_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)[:3]
    combos = detect_combos(orders)
    
    return {
        "favorites": [{"name": item, "count": count} for item, count in favorites],
        "categories": [{"name": cat, "count": count} for cat, count in favorite_categories],
        "average_item_price": round(sum(price_range) / len(price_range), 2) if price_range else 0,
        "unique_items": len(set(all_items)),
        "combos": combos,
        "total_items_ordered": len(all_items)
    }

def detect_combos(orders: List[Dict]) -> List[Dict]:
    combo_count = {}
    
    for order in orders:
        items = [item["name"] for item in order["items"]]
        if len(items) >= 2:
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    combo_key = tuple(sorted([items[i], items[j]]))
                    combo_count[combo_key] = combo_count.get(combo_key, 0) + 1
    
    top_combos = sorted(combo_count.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return [
        {
            "items": list(combo[0]),
            "frequency": combo[1],
            "orders": len(orders)
        }
        for combo in top_combos
    ]

def detect_spending_pattern(orders: List[Dict]) -> Dict:
    amounts = [order["total"] for order in orders]
    avg_amount = sum(amounts) / len(amounts)
    
    if len(amounts) >= 3:
        first_half = sum(amounts[:len(amounts)//2]) / (len(amounts)//2) if len(amounts)//2 > 0 else amounts[0]
        second_half = sum(amounts[len(amounts)//2:]) / (len(amounts)//2) if len(amounts)//2 > 0 else amounts[-1]
        
        if second_half > first_half * 1.1:
            trend = "increasing"
        elif second_half < first_half * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "stable"
    
    return {
        "average": round(avg_amount, 2),
        "min": round(min(amounts), 2),
        "max": round(max(amounts), 2),
        "total_spent": round(sum(amounts), 2),
        "trend": trend,
        "orders_analyzed": len(amounts)
    }

def calculate_streak(orders: List[Dict]) -> int:
    if not orders:
        return 0
    
    sorted_orders = sorted(orders, key=lambda x: x["timestamp"], reverse=True)
    
    streak = 1
    for i in range(len(sorted_orders) - 1):
        diff = (sorted_orders[i]["timestamp"] - sorted_orders[i + 1]["timestamp"]).days
        if diff <= 1:
            streak += 1
        else:
            break
    
    return streak

def detect_timing_pattern(orders: List[Dict]) -> Dict:
    if len(orders) < 3:
        return {"pattern": "unknown", "confidence": 0.0}
    
    sorted_orders = sorted(orders, key=lambda x: x["timestamp"])
    gaps = []
    
    for i in range(len(sorted_orders) - 1):
        diff = (sorted_orders[i + 1]["timestamp"] - sorted_orders[i]["timestamp"]).days
        gaps.append(diff)
    
    avg_gap = sum(gaps) / len(gaps) if gaps else 0
    
    if avg_gap <= 1:
        pattern = "daily"
        confidence = 0.9
    elif avg_gap <= 2:
        pattern = "every_2_days"
        confidence = 0.7
    elif avg_gap <= 4:
        pattern = "weekly"
        confidence = 0.5
    else:
        pattern = "sporadic"
        confidence = 0.3
    
    return {
        "pattern": pattern,
        "average_gap": round(avg_gap, 1),
        "min_gap": min(gaps) if gaps else 0,
        "max_gap": max(gaps) if gaps else 0,
        "confidence": confidence,
        "orders_analyzed": len(orders)
    }


if __name__ == "__main__":
    port = int(os.getenv("PATTERN_SERVICE_PORT", 8001))
    uvicorn.run(app, host="127.0.0.1", port=port)