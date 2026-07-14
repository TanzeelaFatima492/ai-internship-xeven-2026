from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import json
from fastapi.responses import StreamingResponse
import io

from app.services.pinecone_store import pinecone_store
from app.services.embedding_service import embedding_service
from app.services.llm import llm_service
from app.database.base import get_db
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.conversation import Conversation
from app.auth.auth import get_current_user

router = APIRouter(prefix="/rag", tags=["RAG Query"])

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

@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        question_embedding = embedding_service.embed_text(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")
    distances, chunk_ids = pinecone_store.search(question_embedding, request.top_k)
    if not chunk_ids:
        raise HTTPException(status_code=404, detail="No matching documents found.")
    sources, context_chunks = [], []
    for i, chunk_id in enumerate(chunk_ids):
        chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
        if chunk:
            doc = db.query(Document).filter(Document.id == chunk.document_id).first()
            sources.append(SourceInfo(text=chunk.content[:200], document_name=doc.filename if doc else "Unknown", similarity_score=round(1 / (1 + distances[i]), 4) if i < len(distances) else 0))
            context_chunks.append(chunk.content)
    try:
        answer = llm_service.generate_answer(request.question, context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Answer generation failed: {str(e)}")
    conversation = Conversation(thread_id=request.conversation_id or f"{request.question[:40].replace(' ', '_')}", question=request.question, answer=answer, sources=json.dumps([s.model_dump() for s in sources]), user_id=user.id)
    db.add(conversation); db.commit()
    return QueryResponse(question=request.question, answer=answer, sources=sources)

@router.get("/threads")
def list_threads(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role == 'admin':
        threads = db.query(Conversation.thread_id, Conversation.question).order_by(Conversation.created_at.desc()).all()
    else:
        threads = db.query(Conversation.thread_id, Conversation.question).filter(
    Conversation.user_id == user.id,
    Conversation.user_id.isnot(None)
      ).order_by(Conversation.created_at.desc()).all()
    
    result, seen = [], set()
    for t in threads:
        tid = t[0]
        if tid not in seen:
            seen.add(tid)
            # Show first question as title, not PDF name
            title = t[1][:50] if t[1] else tid
            result.append({"thread_id": tid, "title": title})
    return result

@router.get("/threads/{thread_id}")
def get_thread(thread_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    q = db.query(Conversation).filter(Conversation.thread_id == thread_id)
    if user.role != 'admin':
        q = q.filter(Conversation.user_id == user.id)
    messages = q.order_by(Conversation.created_at).all()
    if not messages:
        raise HTTPException(status_code=404, detail="Thread not found")
    return [{"id": m.id, "thread_id": m.thread_id, "question": m.question, "answer": m.answer, "sources": m.sources, "created_at": str(m.created_at) if m.created_at else None} for m in messages]

@router.get("/export/{thread_id}")
def export_thread(thread_id: str, db: Session = Depends(get_db)):
    messages = db.query(Conversation).filter(Conversation.thread_id == thread_id).order_by(Conversation.created_at).all()
    if not messages:
        raise HTTPException(status_code=404, detail="Thread not found")
    export_data = [{"id": m.id, "question": m.question, "answer": m.answer, "sources": json.loads(m.sources) if m.sources else [], "timestamp": str(m.created_at)} for m in messages]
    json_str = json.dumps(export_data, indent=2)
    return StreamingResponse(io.BytesIO(json_str.encode()), media_type="application/json", headers={"Content-Disposition": f"attachment; filename=thread_{thread_id}.json"})