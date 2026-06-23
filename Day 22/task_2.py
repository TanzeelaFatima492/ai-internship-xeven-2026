import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================
# MODEL
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# STORAGE
# =========================
documents = []
metadata = []
index = None


# =========================
# SIMPLE CHUNKER (NO LANGCHAIN DEPENDENCY)
# =========================
def simple_chunk(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


# =========================
# LOAD DOCUMENTS
# =========================
def load_documents(folder="documents"):
    global documents, metadata

    documents.clear()
    metadata.clear()

    if not os.path.exists(folder):
        print("❌ documents folder not found!")
        return

    files = [f for f in os.listdir(folder) if f.endswith(".txt")]

    if not files:
        print("❌ No .txt files found in documents folder!")
        return

    for file in files:
        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            continue

        section = text.split("\n")[0][:100]

        chunks = simple_chunk(text)

        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadata.append({
                "source": file,
                "section": section,
                "chunk_id": i
            })

    print(f"✅ Loaded {len(documents)} chunks from {len(files)} files.")


# =========================
# BUILD FAISS INDEX
# =========================
def build_index():
    global index

    if len(documents) == 0:
        print("❌ No documents loaded. Please load documents first.")
        return

    print("⏳ Building FAISS index...")

    embeddings = model.encode(documents)
    embeddings = np.array(embeddings).astype("float32")

    if embeddings.ndim == 1:
        print("❌ Embedding error: invalid shape")
        return

    # cosine similarity
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print("✅ FAISS index built successfully!")


# =========================
# SEARCH FUNCTION
# =========================
def search(query, k=5, filter_source=None, filter_section=None):
    global index

    if index is None:
        print("❌ Index not built. Please load + build index first.")
        return

    if len(documents) == 0:
        print("❌ No data available.")
        return

    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    faiss.normalize_L2(query_vec)

    distances, indices = index.search(query_vec, len(documents))

    results = []
    seen = set()

    for idx, score in zip(indices[0], distances[0]):

        if idx in seen:
            continue
        seen.add(idx)

        meta = metadata[idx]

        # filters
        if filter_source and meta["source"] != filter_source:
            continue

        if filter_section and filter_section.lower() not in meta["section"].lower():
            continue

        results.append({
            "text": documents[idx],
            "metadata": meta,
            "score": float(score)
        })

        if len(results) == k:
            break

    if not results:
        print("⚠️ No results found.")
        return

    for i, r in enumerate(results):
        print("\n====================")
        print(f"Rank: {i+1}")
        print(f"Source: {r['metadata']['source']}")
        print(f"Section: {r['metadata']['section']}")
        print(f"Chunk ID: {r['metadata']['chunk_id']}")
        print(f"Score: {r['score']:.4f}")
        print("Text:", r["text"][:300])


# =========================
# SHOW DOCUMENTS
# =========================
def show_docs():
    if not documents:
        print("❌ No documents loaded.")
        return

    for i, doc in enumerate(documents[:10]):
        print(f"\n{i+1}. {doc[:200]}")


# =========================
# MENU SYSTEM
# =========================
while True:

    print("\n==============================")
    print("   FAISS DOCUMENT LIBRARY")
    print("==============================")
    print("1. Load Documents")
    print("2. Build FAISS Index")
    print("3. Search Top 5")
    print("4. Search with Filter")
    print("5. Show Sample Chunks")
    print("6. Exit")

    choice = input("Enter choice: ").strip()

    try:

        if choice == "1":
            load_documents()

        elif choice == "2":
            build_index()

        elif choice == "3":
            q = input("Enter query: ")
            search(q, k=5)

        elif choice == "4":
            q = input("Enter query: ")
            src = input("Filter source (Enter skip): ").strip()
            sec = input("Filter section (Enter skip): ").strip()

            search(
                q,
                k=5,
                filter_source=src if src else None,
                filter_section=sec if sec else None
            )

        elif choice == "5":
            show_docs()

        elif choice == "6":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice")

    except KeyboardInterrupt:
        print("\n⚠️ Stopped safely by user.")
    except Exception as e:
        print(f"❌ Error: {e}")