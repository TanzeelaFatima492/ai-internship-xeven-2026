from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.document import Document
from app.models.chunk import Chunk
from app.schemas.document import DocumentResponse
from app.services.document_service import save_uploaded_file
from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.services.embedding_service import embedding_service
from app.services.pinecone_store import pinecone_store

router = APIRouter(prefix="/rag/admin", tags=["Documents"])
pdf_service = PDFService()
chunk_service = ChunkService()

@router.get("/", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()

@router.get("/view/{filename}")
def view_document(filename: str):
    file_path = Path("data/uploads") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/pdf")

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed = [".pdf", ".txt"]
    extension = Path(file.filename).suffix.lower()
    if extension not in allowed:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are allowed.")

    saved_path, size = save_uploaded_file(file)

    document = Document(filename=Path(saved_path).name, file_type=extension)
    db.add(document)
    db.commit()
    db.refresh(document)

    # Extract, chunk, embed, store
    text = pdf_service.extract_text(str(saved_path))
    chunks = chunk_service.split_text(text)

    for chunk_text in chunks:
        chunk = Chunk(document_id=document.id, content=chunk_text)
        db.add(chunk)
        db.commit()
        db.refresh(chunk)

    # Index in Pinecone
    all_chunks = db.query(Chunk).filter(Chunk.document_id == document.id).all()
    embeddings = embedding_service.embed_texts([c.content for c in all_chunks])
    pinecone_store.add_embeddings(embeddings, [c.id for c in all_chunks])

    return document

@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = Path("data/uploads") / doc.filename
    if file_path.exists():
        file_path.unlink()

    db.query(Chunk).filter(Chunk.document_id == doc_id).delete()
    db.delete(doc)
    db.commit()

    return {"message": "Document deleted"}