import sys, os
sys.path.insert(0, os.getcwd())
import numpy as np

# Create fresh store with matching dimension
from app.services.faiss_store import FAISSStore

def test_faiss_add_search():
    store = FAISSStore(dimension=4)
    # Override loaded index
    import faiss
    store.index = faiss.IndexFlatL2(4)
    store.chunk_ids = []
    
    emb = np.array([[1.0, 0, 0, 0]]).astype('float32')
    store.add_embeddings(emb, [100])
    
    d, ids = store.search(emb, k=1)
    assert ids[0] == 100