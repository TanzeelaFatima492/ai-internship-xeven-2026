import faiss
import numpy as np
import pickle
import os

class FAISSStore:
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = None
        self.chunk_ids = []
        self.index_path = "data/faiss_index"
        self.load_index()
    
    def add_embeddings(self, embeddings, chunk_ids):
        """Add embeddings to FAISS index"""
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
        
        embeddings = np.array(embeddings).astype('float32')
        self.index.add(embeddings)
        self.chunk_ids.extend(chunk_ids)
        self.save_index()
        print(f"✅ Added {len(chunk_ids)} chunks to FAISS. Total: {self.index.ntotal}")
    
    def search(self, query_embedding, k=3):
        """Search for similar vectors"""
        if self.index is None or self.index.ntotal == 0:
            return [], []
        
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        query_embedding = query_embedding.astype('float32')
        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        # Map FAISS indices to your chunk IDs
        result_ids = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunk_ids):
                result_ids.append(self.chunk_ids[idx])
        
        return distances[0].tolist(), result_ids
    
    def save_index(self):
        """Save FAISS index and chunk ID mapping"""
        os.makedirs(self.index_path, exist_ok=True)
        faiss.write_index(self.index, f"{self.index_path}/index.faiss")
        with open(f"{self.index_path}/chunk_ids.pkl", "wb") as f:
            pickle.dump(self.chunk_ids, f)
    
    def load_index(self):
        """Load existing index from disk"""
        index_file = f"{self.index_path}/index.faiss"
        ids_file = f"{self.index_path}/chunk_ids.pkl"
        
        if os.path.exists(index_file) and os.path.exists(ids_file):
            self.index = faiss.read_index(index_file)
            with open(ids_file, "rb") as f:
                self.chunk_ids = pickle.load(f)
            print(f"✅ Loaded FAISS index with {self.index.ntotal} vectors")

# Global instance
faiss_store = FAISSStore()