import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.rag.embedding_service import EmbeddingService

embedder = EmbeddingService()

vector = embedder.embed("Pizza")

print(f"Vector Length: {len(vector)}")