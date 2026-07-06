import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.rag.retrieval import RetrievalService

service = RetrievalService()

print("RetrievalService created successfully!")