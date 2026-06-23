from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float


class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    content: str
    score: float


class HealthResponse(BaseModel):
    status: str
    documents: int
    chunks: int
    memory_usage: str