from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    items = Column(JSON, nullable=False)  # [{"name": "Burger", "price": 10.99, "category": "fast_food"}]
    total = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, cancelled
    timestamp = Column(DateTime, default=datetime.utcnow)

class Offer(Base):
    __tablename__ = "offers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    type = Column(String, nullable=False)  # routine_reminder, streak_protection, re_engagement, combo_deal, milestone_reward
    message = Column(String, nullable=False)
    discount = Column(String, nullable=True)  # "10% off", "Free dessert"
    sent_at = Column(DateTime, default=datetime.utcnow)
    is_claimed = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(String, default="info")  # info, offer, reminder, alert