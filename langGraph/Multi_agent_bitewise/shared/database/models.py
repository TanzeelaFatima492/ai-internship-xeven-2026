from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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
    password_hash = Column(String, nullable=False)  # 👈 Add this
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user")
    offers = relationship("Offer", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    
class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    items = Column(JSON, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, default="pending")
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")

class Offer(Base):
    __tablename__ = "offers"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    discount = Column(String, nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)
    is_claimed = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="offers")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(String, default="info")
    user = relationship("User", back_populates="notifications")
