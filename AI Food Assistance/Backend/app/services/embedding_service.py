from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def embed_text(self, text: str):
        """Convert single text to embedding"""
        return self.model.encode([text])[0]
    
    def embed_texts(self, texts: list):
        """Convert multiple texts to embeddings"""
        return self.model.encode(texts)

# Global instance
embedding_service = EmbeddingService()