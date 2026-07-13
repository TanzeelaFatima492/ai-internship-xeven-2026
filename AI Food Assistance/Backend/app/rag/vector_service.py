import faiss
import numpy as np


class VectorStore:

    def __init__(self):

        self.dimension = 384

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

    def add(self, vectors):

        vectors = np.array(
            vectors,
            dtype="float32"
        )

        self.index.add(vectors)

    def search(self, vector, k=5):

        vector = np.array(
            [vector],
            dtype="float32"
        )

        distances, indices = self.index.search(
            vector,
            k
        )

        return distances, indices