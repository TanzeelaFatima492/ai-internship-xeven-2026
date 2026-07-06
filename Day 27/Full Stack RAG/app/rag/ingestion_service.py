from app.rag.embedding_service import EmbeddingService
from app.rag.index_manager import IndexManager


class IngestionService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.index = IndexManager()

    def ingest_chunk(
        self,
        chunk_id: int,
        text: str
    ):
        """
        Process one chunk and
        store it inside FAISS.
        """
        pass