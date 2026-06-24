import os
import time
import psutil
import logging

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from models import (
    AskRequest,
    SearchRequest
)

from rag import (
    add_document,
    search_documents,
    documents
)

from llm import generate_answer
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Production RAG API"
)

# Logging

logging.basicConfig(
    level=logging.INFO
)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Upload Document
# -------------------------

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        start = time.time()

        content = await file.read()

        text = content.decode("utf-8")

        doc_id, chunks = add_document(
            text,
            file.filename
        )

        logging.info(
            f"Uploaded {file.filename}"
        )

        return {
            "message": "Document indexed successfully",
            "document_id": doc_id,
            "chunks": chunks,
            "processing_time": round(
                time.time() - start,
                2
            )
        }

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -------------------------
# List Documents
# -------------------------

@app.get("/documents")
def get_documents():

    return documents

# -------------------------
# Delete Document
# -------------------------

@app.delete("/documents/{doc_id}")
def delete_document(doc_id: str):

    if doc_id not in documents:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    del documents[doc_id]

    return {
        "message": "Document deleted"
    }

# -------------------------
# Semantic Search
# -------------------------

@app.post("/search")
async def search(
    request: SearchRequest
):

    try:

        results = search_documents(
            request.query,
            request.top_k
        )

        return {
            "results": results
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -------------------------
# Ask RAG
# -------------------------

@app.post("/ask")
async def ask(
    request: AskRequest
):

    try:

        results = search_documents(
            request.query,
            5
        )

        context = "\n".join(
            [r["text"] for r in results]
        )

        answer = generate_answer(
            request.query,
            context
        )

        sources = list(
            set(
                [
                    r["source"]
                    for r in results
                ]
            )
        )

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():

    memory = psutil.Process(
        os.getpid()
    ).memory_info().rss / 1024 / 1024

    return {
        "status": "healthy",
        "document_count": len(documents),
        "memory_usage_mb": round(
            memory,
            2
        )
    }