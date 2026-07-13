from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.document_service import save_uploaded_file

router = APIRouter(
    prefix="/rag/admin",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    allowed = [".pdf", ".txt"]

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed."
        )

    saved_path, size = save_uploaded_file(file)

    document = Document(
        title=Path(file.filename).stem,
        filename=Path(saved_path).name,
        file_type=extension,
        file_size=size,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document