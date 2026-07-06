from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_FOLDER = Path("data/uploads")

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
async def upload_document(

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    if not file.filename.endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="Only PDF files are allowed."

        )

    file_path = UPLOAD_FOLDER / file.filename

    with open(

        file_path,

        "wb"

    ) as buffer:

        buffer.write(

            await file.read()

        )

    document = Document(

        filename=file.filename,

        file_type="pdf"

    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return document