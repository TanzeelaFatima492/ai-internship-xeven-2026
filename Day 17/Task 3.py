import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import networkx as nx

# 1. Create a small corpus of 20 synthetic "documents" (short texts)
documents = [
    # Technology / AI
    "Artificial intelligence is transforming industries with machine learning and deep learning.",
    "Deep neural networks are a subset of machine learning that use multiple layers to extract features.",
    "The latest smartphone features a foldable screen and 5G connectivity.",
    "Cloud computing provides scalable resources on demand for businesses of all sizes.",

    # Health / Nutrition
    "Eating a balanced diet rich in fruits and vegetables can improve overall health.",
    "Regular exercise, such as walking or jogging, reduces the risk of heart disease.",
    "A Mediterranean diet emphasizes olive oil, fish, and fresh vegetables.",
    "Yoga and meditation can reduce stress and promote mental clarity.",

    # Travel / Geography
    "Paris is known for its iconic Eiffel Tower and world-class museums.",
    "The Great Barrier Reef is a vast coral ecosystem off the coast of Australia.",
    "Tokyo offers a blend of traditional temples and futuristic skyscrapers.",
    "Visiting national parks allows tourists to experience untouched natural beauty.",

    # Sports
    "Soccer is the most popular sport globally, with billions of fans.",
    "The FIFA World Cup is held every four years and draws massive audiences.",
    "Basketball requires agility, teamwork, and precise shooting skills.",
    "The Olympics bring together athletes from all over the world to compete.",

    # Finance / Business
    "Investing in index funds is a low-cost way to diversify a portfolio.",
    "Startups often rely on venture capital to scale their operations quickly.",
    "Cryptocurrencies like Bitcoin use blockchain technology for decentralized transactions.",

    # Near‑duplicate: almost identical to one of the tech documents (sim >0.95)
    "Artificial intelligence is transforming industries with machine learning and deep learning techniques."
    # same as doc[0] with just one extra word "techniques"
]

# 2. Load embedding model & encode all documents
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(documents)

# 3. Compute pairwise cosine similarity matrix
sim_matrix = cosine_similarity(embeddings)

# 4. Detect near‑duplicates (similarity > 0.95)
threshold_duplicate = 0.95
n = len(documents)
duplicates = []
for i in range(n):
    for j in range(i+1, n):
        if sim_matrix[i, j] > threshold_duplicate:
            duplicates.append((i, j, sim_matrix[i, j]))

print("=== NEAR‑DUPLICATE DETECTION (sim > 0.95) ===")
if duplicates:
    for i, j, sim in duplicates:
        print(f"Docs {i} & {j} (score: {sim:.4f})")
        print(f"   '{documents[i][:60]}...'")
        print(f"   '{documents[j][:60]}...'")
else:
    print("No near‑duplicates found.")

# 5. Build clusters using similarity threshold (cosine sim ≥ 0.75)
threshold_cluster = 0.75
G = nx.Graph()
G.add_nodes_from(range(n))
for i in range(n):
    for j in range(i+1, n):
        if sim_matrix[i, j] >= threshold_cluster:
            G.add_edge(i, j, weight=sim_matrix[i, j])

# Connected components as clusters
clusters = list(nx.connected_components(G))
# Map document index -> cluster ID
cluster_labels = np.full(n, -1)
for cluster_id, comp in enumerate(clusters):
    for idx in comp:
        cluster_labels[idx] = cluster_id

print("\n=== CLUSTERS (sim ≥ 0.75) ===")
for cid, comp in enumerate(clusters):
    print(f"Cluster {cid}:")
    for idx in comp:
        print(f"  [{idx}] {documents[idx][:70]}...")

# 6. Visualize with t‑SNE, colored by cluster
tsne = TSNE(n_components=2, random_state=42, perplexity=5, metric='cosine')
embeddings_2d = tsne.fit_transform(embeddings)

plt.figure(figsize=(10, 8))
# Plot points, coloring by cluster (grey for unassigned)
unique_clusters = np.unique(cluster_labels)
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_clusters)))
for cid, col in zip(unique_clusters, colors):
    mask = cluster_labels == cid
    if cid == -1:
        col = 'grey'
        label = 'Noise'
    else:
        label = f'Cluster {cid}'
    plt.scatter(embeddings_2d[mask, 0], embeddings_2d[mask, 1],
                c=[col], label=label, s=80, edgecolors='k', alpha=0.8)

# Annotate each point with a short label (first few words)
for i, txt in enumerate(documents):
    short_label = ' '.join(txt.split()[:4])  # first 4 words
    plt.annotate(short_label, (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                 fontsize=8, alpha=0.8, textcoords="offset points", xytext=(0,10),
                 ha='center')

plt.title("Document Embeddings visualized with t‑SNE\ncolored by similarity‑based clusters", fontsize=12)
plt.legend(loc='best')
plt.tight_layout()
plt.show()