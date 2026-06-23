# Task 1: Generate & Compare Embeddings
# ---------------------------------------
# pip install openai numpy matplotlib seaborn --break-system-packages

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer

# ----------------------------------------------------------------------
# 1. Cosine similarity from scratch
# ----------------------------------------------------------------------
def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    Formula: dot(v1, v2) / (||v1|| * ||v2||)
    """
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0   # handle zero vectors gracefully
    return dot / (norm1 * norm2)

# ----------------------------------------------------------------------
# 2. Generate embeddings using OpenAI API
# ----------------------------------------------------------------------


def get_embeddings(texts: list[str]) -> np.ndarray:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    return np.array(embeddings)

# ----------------------------------------------------------------------
# 3. Sample sentences
# ----------------------------------------------------------------------
sentences = [
    "dog",
    "puppy",
    "car",
    "automobile",
    "cat",
    "kitten",
    "house",
    "building",
    "apple",
    "banana"
]

# ----------------------------------------------------------------------
# 4. Main execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Get embeddings
    print("Fetching embeddings from OpenAI...")
    emb = get_embeddings(sentences)

    # --- Highlight specific comparisons ---
    idx_dog = 0
    idx_puppy = 1
    idx_car = 2

    sim_dog_puppy = cosine_similarity(emb[idx_dog], emb[idx_puppy])
    sim_dog_car   = cosine_similarity(emb[idx_dog], emb[idx_car])

    print(f"\nCosine similarity: 'dog' vs 'puppy' → {sim_dog_puppy:.4f}  (expected high)")
    print(f"Cosine similarity: 'dog' vs 'car'   → {sim_dog_car:.4f}  (expected low)")

    # --- Compute full similarity matrix ---
    n = len(sentences)
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            sim_matrix[i][j] = cosine_similarity(emb[i], emb[j])

    # --- Heatmap visualisation ---
    plt.figure(figsize=(10, 8))
    sns.heatmap(sim_matrix,
                xticklabels=sentences,
                yticklabels=sentences,
                annot=True, fmt=".2f", cmap="YlOrRd",
                square=True, linewidths=.5, cbar_kws={"shrink": 0.8})
    plt.title("Cosine Similarity Matrix (OpenAI Embeddings)", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()