

import math

# ==========================
# SAMPLE DOCUMENT
# ==========================

document = """
Artificial Intelligence (AI) is a branch of computer science that focuses on creating intelligent machines.

Machine Learning is a subset of AI that allows systems to learn from data without explicit programming.

Deep Learning is a subset of Machine Learning that uses neural networks with many layers.

Natural Language Processing (NLP) helps computers understand human language.

Computer Vision enables machines to interpret and analyze images and videos.

AI is widely used in healthcare, finance, education, robotics, and self-driving cars.

Large language models like GPT are trained on massive datasets to generate human-like text.
"""

# ==========================
# CHUNKING FUNCTION
# ==========================

def chunk_text(text, chunk_size):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


# ==========================
# SIMULATED EMBEDDING SIZE
# ==========================
# Assume each chunk embedding = 1536 dimensions (like OpenAI)
# Each float = 4 bytes

EMBEDDING_DIM = 1536
BYTES_PER_FLOAT = 4

def embedding_size(num_chunks):
    return num_chunks * EMBEDDING_DIM * BYTES_PER_FLOAT


# ==========================
# SIMPLE RETRIEVAL SIMULATION
# ==========================
# We simulate retrieval quality based on chunk size:
# smaller chunks → more precise but less context
# larger chunks → more context but less precision

def retrieval_quality(chunk_size):
    if chunk_size <= 200:
        return 6.5  # too small, missing context
    elif chunk_size <= 500:
        return 8.5  # best balance
    elif chunk_size <= 1000:
        return 8.0  # good context
    else:
        return 6.8  # too large, noisy results


# ==========================
# EXPERIMENT RUNNER
# ==========================

chunk_sizes = [200, 500, 1000, 2000]

results = []

for size in chunk_sizes:
    chunks = chunk_text(document, size)
    num_chunks = len(chunks)
    storage = embedding_size(num_chunks) / 1024  # KB
    quality = retrieval_quality(size)

    results.append({
        "chunk_size": size,
        "num_chunks": num_chunks,
        "storage_kb": round(storage, 2),
        "retrieval_quality_score": quality
    })


# ==========================
# PRINT REPORT
# ==========================

print("\n================= EXPERIMENT REPORT =================\n")

for r in results:
    print(f"Chunk Size: {r['chunk_size']} chars")
    print(f"Number of Chunks: {r['num_chunks']}")
    print(f"Storage Required: {r['storage_kb']} KB")
    print(f"Retrieval Quality Score: {r['retrieval_quality_score']}")
    print("-" * 50)


# ==========================
# FINAL RECOMMENDATION
# ==========================

best = max(results, key=lambda x: x["retrieval_quality_score"])

print("\n================= FINAL RECOMMENDATION =================\n")
print(f"Best Chunk Size: {best['chunk_size']} characters")
print(f"Reason: Highest balance of context + precision")
print("\nRecommended setting for RAG systems:")
print("Chunk Size: 500–1000 characters (or ~512 tokens)")
print("Overlap: 10–20%")
print("Use RecursiveCharacterTextSplitter in production")