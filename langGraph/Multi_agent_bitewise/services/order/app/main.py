from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict, Optional
import uvicorn
import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.database.models import User, Order
from shared.database.database import get_db, engine, Base

load_dotenv()

# ==================== CREATE TABLES ====================
Base.metadata.create_all(bind=engine)

# ==================== APP ====================
app = FastAPI(
    title="BiteWise Order Service",
    version="1.0.0",
    description="Handles order placement and processing"
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
class OrderItem(BaseModel):
    name: str
    price: float
    category: Optional[str] = None
    quantity: int = 1

class OrderRequest(BaseModel):
    items: List[OrderItem]

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    return {"service": "Order Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/user/{user_id}/order")
async def place_order(user_id: str, items: List[Dict], db: Session = Depends(get_db)):
    """Place a new order"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate total
    total = sum(
        item.get("price", 0) * item.get("quantity", 1)
        for item in items
    )
    
    # Create order
    order = Order(
        user_id=user_id,
        items=items,
        total=total,
        status="confirmed",
        timestamp=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Send notification to notification service
    try:
        requests.post(
            "http://localhost:8003/notify",
            json={
                "user_id": user_id,
                "message": f"✅ Your order has been placed successfully! Total: ${total:.2f}",
                "type": "order_confirmation"
            }
        )
    except Exception:
        pass  # Notification service might not be running
    
    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "total": total,
        "status": order.status
    }

# ==================== MAIN ====================
if __name__ == "__main__":
    port = int(os.getenv("ORDER_SERVICE_PORT", 8006))
    uvicorn.run(app, host="127.0.0.1", port=port)
