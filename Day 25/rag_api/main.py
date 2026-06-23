import time
import psutil

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from document_manager import DocumentManager
from rag_service import RAGService

from models import (
    AskRequest,
    SearchRequest
)

from logger import logger


app = FastAPI(
    title="Production RAG API",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Global Services
# =========================

document_manager = None
rag_service = None


# =========================
# Request Logging Middleware
# =========================

@app.middleware("http")
async def log_requests(request, call_next):

    start_time = time.time()

    try:

        response = await call_next(request)

        process_time = round(
            time.time() - start_time,
            3
        )

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"Status={response.status_code} "
            f"Time={process_time}s"
        )

        return response

    except Exception as e:

        logger.error(str(e))

        raise


# =========================
# Startup Event
# =========================

@app.on_event("startup")
async def startup_event():

    global document_manager
    global rag_service

    logger.info("Loading services...")

    document_manager = DocumentManager()

    rag_service = RAGService()

    logger.info("Services loaded successfully")


# =========================
# Health Check
# =========================

@app.get("/health")
async def health():

    try:

        memory = psutil.Process().memory_info().rss

        memory_mb = round(
            memory / 1024 / 1024,
            2
        )

        return {
            "status": "healthy",
            "documents":
                document_manager.get_document_count(),
            "chunks":
                document_manager.get_chunk_count(),
            "memory_usage":
                f"{memory_mb} MB",
            "index_loaded":
                rag_service.vectorstore is not None
        }

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Upload Document
# =========================

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        filepath = (
            document_manager
            .save_uploaded_file(file)
        )

        result = (
            document_manager
            .upload_document(
                filepath,
                file.filename
            )
        )

        rag_service.reload_index()

        logger.info(
            f"Document uploaded: "
            f"{file.filename}"
        )

        return result

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# List Documents
# =========================

@app.get("/documents")
async def list_documents():

    try:

        return (
            document_manager
            .list_documents()
        )

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Delete Document
# =========================

@app.delete("/documents/{document_id}")
async def delete_document(
    document_id: str
):

    try:

        document_manager.delete_document(
            document_id
        )

        rag_service.reload_index()

        return {
            "message":
                "Document deleted successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Semantic Search
# =========================

@app.post("/search")
async def semantic_search(
    request: SearchRequest
):

    try:

        results = rag_service.search(
            request.query
        )

        return {
            "results": results
        }

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Ask Endpoint
# =========================

@app.post("/ask")
async def ask_question(
    request: AskRequest
):

    try:

        result = (
            await rag_service.generate_answer(
                request.question
            )
        )

        return result

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Root
# =========================

@app.get("/")
async def root():

    return {
        "message":
            "Production RAG API Running"
    }