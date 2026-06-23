import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

  
# DOCUMENTS
  
documents = [
    "FAISS is a library for fast similarity search using vectors",
    "BM25 is a keyword-based ranking algorithm",
    "Hybrid search combines semantic and keyword retrieval",
    "RAG uses retrieval augmented generation for AI answers",
    "Re-ranking improves retrieval precision using LLM scoring",
    "Embeddings convert text into vector representations",
    "Vector databases store high-dimensional embeddings",
    "LLMs can evaluate relevance of retrieved documents",
    "Search systems often combine retrieval and ranking stages",
    "FAISS supports large-scale similarity search efficiently"
]

  
# EMBEDDINGS + FAISS INDEX
  
model = SentenceTransformer("all-MiniLM-L6-v2")

doc_embeddings = model.encode(documents)
doc_embeddings = np.array(doc_embeddings).astype("float32")

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings)

  
# RETRIEVAL (TOP 20)
  
def retrieve_top_k(query, k=20):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append(documents[idx])
    return results

  
# LLM SCORING (SIMULATED)
  
# (Replace this with OpenAI / GPT API later)
def llm_score(query, chunk):

    query_words = set(query.lower().split())
    chunk_words = set(chunk.lower().split())

    overlap = len(query_words.intersection(chunk_words))

    # simple scoring logic (0–10)
    score = min(10, overlap * 2 + np.random.uniform(0, 2))

    return round(score, 2)

  
# RE-RANKING
  
def rerank(query, retrieved_chunks, top_n=5):

    scored_chunks = []

    for chunk in retrieved_chunks:
        score = llm_score(query, chunk)
        scored_chunks.append((chunk, score))

    # sort by score (high → low)
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return scored_chunks[:top_n]

  
# FULL PIPELINE
  
def rag_pipeline(query):

    print("\n🔍 Query:", query)

    # Step 1: Retrieve top 20 (or all if small dataset)
    retrieved = retrieve_top_k(query, k=20)

    print("\n📥 Retrieved Chunks:", len(retrieved))

    # Step 2: Re-rank
    reranked = rerank(query, retrieved, top_n=5)

    print("\n🏆 Top 5 After Re-ranking:\n")

    for i, (chunk, score) in enumerate(reranked, 1):
        print(f"{i}. (Score: {score}) {chunk}")

    return reranked

  
# TEST
  
query = "How does re-ranking improve retrieval in RAG systems?"
rag_pipeline(query)