from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database.base import get_db
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.chunk import Chunk

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    """Get system overview stats"""
    
    total_queries = db.query(Conversation).count()
    total_documents = db.query(Document).count()
    total_chunks = db.query(Chunk).count()
    total_threads = db.query(Conversation.thread_id).distinct().count()
    
    return {
        "total_queries": total_queries,
        "total_documents": total_documents,
        "total_chunks": total_chunks,
        "total_threads": total_threads
    }

@router.get("/popular-questions")
def popular_questions(db: Session = Depends(get_db), limit: int = 10):
    """Get most asked questions"""
    
    questions = db.query(
        Conversation.question,
        func.count(Conversation.id).label("count")
    ).group_by(Conversation.question)\
     .order_by(func.count(Conversation.id).desc())\
     .limit(limit).all()
    
    return [
        {"question": q[0], "count": q[1]}
        for q in questions
    ]

@router.get("/recent-queries")
def recent_queries(db: Session = Depends(get_db), limit: int = 10):
    """Get recent queries"""
    
    queries = db.query(Conversation)\
        .order_by(Conversation.created_at.desc())\
        .limit(limit).all()
    
    return [
        {
            "id": q.id,
            "thread_id": q.thread_id,
            "question": q.question,
            "answer": q.answer[:100] + "..." if len(q.answer) > 100 else q.answer,
            "created_at": str(q.created_at)
        }
        for q in queries
    ]

@router.get("/daily-usage")
def daily_usage(db: Session = Depends(get_db)):
    """Get query count per day"""
    
    usage = db.query(
        func.date(Conversation.created_at).label("date"),
        func.count(Conversation.id).label("count")
    ).group_by(func.date(Conversation.created_at))\
     .order_by(func.date(Conversation.created_at).desc())\
     .limit(30).all()
    
    return [
        {"date": str(u[0]), "queries": u[1]}
        for u in usage
    ]