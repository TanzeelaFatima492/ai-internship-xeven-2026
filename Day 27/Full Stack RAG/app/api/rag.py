from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from app.services.faiss_store import faiss_store
from app.services.embedding_service import embedding_service
from app.services.llm import llm_service
from app.database.base import get_db
from app.models.document import Document
from app.models.chunk import Chunk

router = APIRouter(prefix="/rag", tags=["RAG Query"])

# ---------- Schemas ----------
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

class SourceInfo(BaseModel):
    text: str
    document_name: str
    similarity_score: float

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceInfo]

# ---------- Endpoint ----------
@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest, db: Session = Depends(get_db)):
    
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
                text=chunk.content[:200],  # Changed from .text to .content
                document_name=doc.filename if doc else "Unknown",
                similarity_score=round(1 / (1 + distances[i]), 4) if i < len(distances) else 0
            ))
            context_chunks.append(chunk.content)  # Changed from .text to .content
    
    # 4. Generate answer via LLM
    try:
        answer = llm_service.generate_answer(request.question, context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Answer generation failed: {str(e)}")
    
    return QueryResponse(
        question=request.question,
        answer=answer,
        sources=sources
    )