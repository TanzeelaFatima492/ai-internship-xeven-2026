import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import uuid

# =====================
# GLOBALS
# =====================
model = SentenceTransformer("all-MiniLM-L6-v2")

documents = {}
index = None
dim = 384


# =====================
# INIT INDEX (FIXED)
# =====================
def init_index():
    global index
    index = faiss.IndexFlatL2(dim)


# =====================
# CHUNK FUNCTION
# =====================
def chunk_text(text, chunk_size=200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


# =====================
# ADD DOCUMENT
# =====================
def add_document(text, metadata):
    global index

    chunks = chunk_text(text)
    embeddings = model.encode(chunks).astype("float32")

    ids = []

    for i, chunk in enumerate(chunks):
        doc_id = str(uuid.uuid4())

        documents[doc_id] = {
            "text": chunk,
            "metadata": metadata
        }

        index.add(np.array([embeddings[i]]))
        ids.append(doc_id)

    return ids


# =====================
# SEARCH
# =====================
def search(query, k=5):
    query_vec = model.encode([query]).astype("float32")

    D, I = index.search(query_vec, k)

    results = []

    doc_ids = list(documents.keys())

    for i in I[0]:
        if i < len(doc_ids):
            doc_id = doc_ids[i]
            results.append(documents[doc_id])

    return results