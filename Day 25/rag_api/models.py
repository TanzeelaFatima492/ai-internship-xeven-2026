from pydantic import BaseModel
from typing import List, Optional


class AskRequest(BaseModel):
    query: str


class UploadResponse(BaseModel):
    message: str
    doc_ids: List[str]


class SearchResponse(BaseModel):
    results: List[dict]


class HealthResponse(BaseModel):
    status: str
    total_documents: int