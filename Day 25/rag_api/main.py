from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AskRequest
import time
import logging
from groq import Groq
from fastapi import HTTPException
from rag import init_index, add_document, search, documents

app = FastAPI(title="RAG API")

#     CORS    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#     LOGGING    
logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
async def startup():
    init_index()
    logging.info("RAG system started")


#     UPLOAD    
@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        start = time.time()

        content = await file.read()
        text = content.decode("utf-8")

        doc_ids = add_document(text, {"filename": file.filename})

        logging.info(f"Uploaded {file.filename} in {time.time()-start:.2f}s")

        return {"message": "uploaded", "doc_ids": doc_ids}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#     LIST DOCS    
@app.get("/documents")
async def get_documents():
    return documents


#     DELETE    
@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")

    del documents[doc_id]
    return {"message": "deleted"}


#     ASK RAG    
@app.post("/ask")
async def ask(req: AskRequest):
    try:
        results = search(req.query)

        context_chunks = [r["text"] for r in results]

        answer = generate_answer(req.query, context_chunks)

        return {
            "answer": answer,
            "sources": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#     SEMANTIC SEARCH ONLY    
@app.post("/search")
async def semantic_search(req: AskRequest):
    try:
        results = search(req.query)
        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#     HEALTH    
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "total_documents": len(documents)
    }