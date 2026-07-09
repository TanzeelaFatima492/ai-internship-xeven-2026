import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

class PineconeStore:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = "menu-rag"
        
        # Create index if not exists
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        self.index = self.pc.Index(self.index_name)
        print(f"✅ Pinecone connected ({self.index.describe_index_stats()['total_vector_count']} vectors)")
    
    def add_embeddings(self, embeddings, chunk_ids):
        """Add embeddings to Pinecone"""
        vectors = []
        for i, (emb, cid) in enumerate(zip(embeddings, chunk_ids)):
            vectors.append({
                "id": str(cid),
                "values": emb.tolist(),
                "metadata": {"chunk_id": cid}
            })
        
        # Batch upsert
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            self.index.upsert(vectors=vectors[i:i+batch_size])
        
        print(f"✅ Added {len(vectors)} chunks to Pinecone")
    
    def search(self, query_embedding, k=3):
        """Search Pinecone"""
        results = self.index.query(
            vector=query_embedding.tolist(),
            top_k=k,
            include_metadata=True
        )
        
        distances = []
        chunk_ids = []
        for match in results["matches"]:
            distances.append(1 - match["score"])  # Convert cosine to distance
            chunk_ids.append(int(match["metadata"]["chunk_id"]))
        
        return distances, chunk_ids
    
    def clear(self):
        """Delete all vectors"""
        self.index.delete(delete_all=True)
        print("✅ Pinecone cleared")

# Global instance
pinecone_store = PineconeStore()