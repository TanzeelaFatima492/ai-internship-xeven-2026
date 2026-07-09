from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.document import Document
from app.models.chunk import Chunk
from app.schemas.document import DocumentResponse
from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.services.embedding_service import embedding_service
from app.services.pinecone_store import pinecone_store

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_FOLDER = Path("data/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

pdf_service = PDFService()
chunk_service = ChunkService()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 1. Save file
    file_path = UPLOAD_FOLDER / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2. Save document record
    document = Document(filename=file.filename, file_type="pdf")
    db.add(document)
    db.commit()
    db.refresh(document)

    # 3. Extract text from PDF
    try:
        text = pdf_service.extract_text(str(file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {str(e)}")

    # 4. Chunk the text
    chunks = chunk_service.split_text(text)
    if not chunks:
        raise HTTPException(status_code=500, detail="No text extracted from PDF.")

    # 5. Generate embeddings
    embeddings = embedding_service.embed_texts(chunks)

    # 6. Save chunks to DB
    chunk_ids = []
    for chunk_text in chunks:
        chunk = Chunk(document_id=document.id, content=chunk_text)
        db.add(chunk)
        db.commit()
        db.refresh(chunk)
        chunk_ids.append(chunk.id)

    # 7. Store in FAISS
    pinecone_store.add_embeddings(embeddings, chunk_ids)

    return document