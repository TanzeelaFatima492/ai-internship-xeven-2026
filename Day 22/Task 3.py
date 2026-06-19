import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. DATASET
documents = [
    "Artificial Intelligence is transforming the world",
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "FAISS is a library for efficient similarity search",
    "Chroma is a vector database with persistence",
    "Python is widely used in AI development",
    "Vector databases store embeddings",
    "Embeddings represent text in vector form"
]

# 2. EMBEDDINGS (TF-IDF)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents).toarray().astype("float32")

query_text = ["What is AI?"]
query_vector = vectorizer.transform(query_text).toarray().astype("float32")

print("\n=========================")
print("Embedding shape:", X.shape)
print("=========================\n")


# 3. FAISS IMPLEMENTATION
import faiss

dimension = X.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)

# Indexing time (FAISS)
start = time.time()
faiss_index.add(X)
faiss_index_time = time.time() - start

# Query time (FAISS)
start = time.time()
D, I = faiss_index.search(query_vector, k=3)
faiss_query_time = time.time() - start

faiss_results = I[0]

# 4. CHROMADB IMPLEMENTATION
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="vector_demo")

# Indexing time (Chroma)
start = time.time()

for i, doc in enumerate(documents):
    collection.add(
        ids=[str(i)],
        documents=[doc],
        embeddings=[X[i].tolist()]
    )

chroma_index_time = time.time() - start

# Query time (Chroma)
start = time.time()
results = collection.query(
    query_embeddings=query_vector.tolist(),
    n_results=3
)
chroma_query_time = time.time() - start

chroma_results = results["documents"][0]


# 5. OUTPUT RESULTS
print("\n================ FAISS RESULTS ================")
for idx in faiss_results:
    print(documents[idx])

print("\nFAISS Index Time:", faiss_index_time)
print("FAISS Query Time:", faiss_query_time)


print("\n================ CHROMA RESULTS ================")
for doc in chroma_results:
    print(doc)

print("\nChroma Index Time:", chroma_index_time)
print("Chroma Query Time:", chroma_query_time)

# 6. COMPARISON SUMMARY
print("\n================ COMPARISON =================")

print(f"FAISS Indexing Time  : {faiss_index_time:.6f} sec")
print(f"Chroma Indexing Time : {chroma_index_time:.6f} sec")

print(f"\nFAISS Query Time     : {faiss_query_time:.6f} sec")
print(f"Chroma Query Time    : {chroma_query_time:.6f} sec")

print("\nFEATURE COMPARISON:")
print("- FAISS   → Fast, lightweight, in-memory search")
print("- Chroma  → Persistent storage, metadata support, production ready")