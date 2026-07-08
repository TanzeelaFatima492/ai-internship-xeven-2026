from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import json
from fastapi.responses import StreamingResponse
import io

from app.services.faiss_store import faiss_store
from app.services.embedding_service import embedding_service
from app.services.llm import llm_service
from app.database.base import get_db
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.conversation import Conversation
from app.auth.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/rag", tags=["RAG Query"])

# ---------- Schemas ----------
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    conversation_id: Optional[str] = None

class SourceInfo(BaseModel):
    text: str
    document_name: str
    similarity_score: float

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceInfo]

class ConversationResponse(BaseModel):
    id: int
    thread_id: str
    question: str
    answer: str
    sources: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

# ---------- Query Endpoint ----------
@router.post("/query", response_model=QueryResponse)
@limiter.limit("5/minute")
def query_rag(request: QueryRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    
    # 1. Embed the question
    try:
        question_embedding = embedding_service.embed_text(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")
    
    # 2. Search FAISS
    distances, chunk_ids = faiss_store.search(question_embedding, request.top_k)
    
    if not chunk_ids:
        raise HTTPException(status_code=404, detail="No matching documents found. Upload a menu first.")
    
    # 3. Get chunk texts from DB
    sources = []
    context_chunks = []
    
    for i, chunk_id in enumerate(chunk_ids):
        chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
        if chunk:
            doc = db.query(Document).filter(Document.id == chunk.document_id).first()
            sources.append(SourceInfo(
                text=chunk.content[:200],
                document_name=doc.filename if doc else "Unknown",
                similarity_score=round(1 / (1 + distances[i]), 4) if i < len(distances) else 0
            ))
            context_chunks.append(chunk.content)
    
    # 4. Generate answer via LLM
    try:
        answer = llm_service.generate_answer(request.question, context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Answer generation failed: {str(e)}")
    
    # 5. Save conversation to DB
    conversation = Conversation(
        thread_id=request.conversation_id or f"thread_{sources[0].document_name}",
        question=request.question,
        answer=answer,
        sources=json.dumps([s.model_dump() for s in sources])
    )
    db.add(conversation)
    db.commit()
    
    return QueryResponse(
        question=request.question,
        answer=answer,
        sources=sources
    )

# ---------- Thread Endpoints ----------
@router.get("/threads")
def list_threads(db: Session = Depends(get_db)):
    """List all conversation threads"""
    threads = db.query(Conversation.thread_id).distinct().all()
    return [{"thread_id": t[0]} for t in threads]

@router.get("/threads/{thread_id}")
def get_thread(thread_id: str, db: Session = Depends(get_db)):
    messages = db.query(Conversation).filter(
        Conversation.thread_id == thread_id
    ).order_by(Conversation.created_at).all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    result = []
    for m in messages:
        result.append({
            "id": m.id,
            "thread_id": m.thread_id,
            "question": m.question,
            "answer": m.answer,
            "sources": m.sources,
            "created_at": str(m.created_at) if m.created_at else None
        })
    
    return result


@router.get("/export/{thread_id}")
def export_thread(thread_id: str, db: Session = Depends(get_db)):
    """Download thread as JSON file"""
    messages = db.query(Conversation).filter(
        Conversation.thread_id == thread_id
    ).order_by(Conversation.created_at).all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    export_data = []
    for m in messages:
        export_data.append({
            "id": m.id,
            "question": m.question,
            "answer": m.answer,
            "sources": json.loads(m.sources) if m.sources else [],
            "timestamp": str(m.created_at)
        })
    
    json_str = json.dumps(export_data, indent=2)
    
    return StreamingResponse(
        io.BytesIO(json_str.encode()),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=thread_{thread_id}.json"}
    )