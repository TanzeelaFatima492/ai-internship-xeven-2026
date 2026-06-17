# Day 17: Learnings

Today, I learned about embeddings and how Large Language Models (LLMs) represent text numerically. Although computers fundamentally process binary data (0s and 1s), AI models convert text into tokens and assign each token a unique token ID. These token IDs are then transformed into embedding vectors, which are numerical representations that capture the semantic meaning of words and sentences.

I explored embedding models such as `text-embedding-3-small` and `text-embedding-3-large` and understood that higher dimensions allow models to capture richer semantic relationships. I learned that semantic means the meaning of text, while semantic similarity measures how close two pieces of text are in meaning.

I studied three similarity metrics: cosine similarity, dot product, and Euclidean distance. Cosine similarity is widely used because it compares the direction of vectors and works well for semantic search and Retrieval-Augmented Generation (RAG).

I also learned why vector databases are important. Traditional databases perform exact keyword matching, whereas vector databases store embeddings and efficiently find semantically similar information. This technology powers semantic search, recommendation systems, document clustering, duplicate detection, and modern AI applications. Implementing cosine similarity from scratch and visualizing a similarity matrix helped me understand how embeddings are compared mathematically.
