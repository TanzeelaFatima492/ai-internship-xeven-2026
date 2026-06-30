
     
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

      
# SAMPLE DOCUMENTS
      
documents = [
    "FAISS is a library for similarity search using embeddings",
    "BM25 is a keyword-based ranking algorithm",
    "Hybrid search combines semantic and keyword search",
    "RAG systems use retrieval augmented generation",
    "FAISS helps in fast vector similarity search"
]

     
# BM25 (KEYWORD INDEX)
      
tokenized_docs = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

      
# FAISS (SEMANTIC INDEX)
     
model = SentenceTransformer("all-MiniLM-L6-v2")

doc_embeddings = model.encode(documents)
doc_embeddings = np.array(doc_embeddings).astype("float32")

dimension = doc_embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(doc_embeddings)

     
# QUERY FUNCTION
      
def hybrid_search(query, top_k=3):

    #   FAISS  
    query_vec = model.encode([query]).astype("float32")
    distances, indices = faiss_index.search(query_vec, top_k)

    faiss_scores = {}
    for rank, idx in enumerate(indices[0]):
        score = 1 / (1 + distances[0][rank])  # convert distance → similarity
        faiss_scores[documents[idx]] = score

    #   BM25  
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)

    # normalize BM25
    bm25_scores = np.array(bm25_scores)
    bm25_norm = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-6)

    bm25_dict = {documents[i]: bm25_norm[i] for i in range(len(documents))}

    #   HYBRID FUSION  
    final_scores = {}

    for doc in documents:
        final_scores[doc] = (
            0.7 * faiss_scores.get(doc, 0) +
            0.3 * bm25_dict.get(doc, 0)
        )

    # sort results
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    return ranked
      
# TEST QUERY

query = "What is hybrid search in FAISS and BM25?"
results = hybrid_search(query)

print("\n Final Hybrid Search Results:\n")
for doc, score in results:
    print(f"{score:.4f} -> {doc}")