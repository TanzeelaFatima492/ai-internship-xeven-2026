from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.rag.embedding_service import EmbeddingService
from app.rag.index_manager import IndexManager


class IngestionService:

    def __init__(self):

        self.pdf_service = PDFService()

        self.chunk_service = ChunkService()

        self.embedding_service = EmbeddingService()

        self.index_manager = IndexManager()

    def ingest_pdf(
        self,
        file_path: str
    ):

        # Step 1
        text = self.pdf_service.extract_text(file_path)

        # Step 2
        chunks = self.chunk_service.split_text(text)

        # Step 3
        embeddings = self.embedding_service.embed_documents(chunks)

        # Step 4
        self.index_manager.add_vectors(
            embeddings,
            chunks
        )

        # Step 5
        self.index_manager.save()

        return len(chunks)