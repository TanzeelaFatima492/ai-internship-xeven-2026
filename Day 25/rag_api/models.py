from pydantic import BaseModel
from typing import List


class AskRequest(BaseModel):
    query: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: List[str]