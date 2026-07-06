from app.rag.embedding_service import EmbeddingService
from app.rag.index_manager import IndexManager


class RetrievalService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.index_manager = IndexManager()

    def search(
        self,
        query: str,
        k: int = 5
    ):
        """
        Search for the top-k most similar chunks.

        Implementation will be added next.
        """
        pass