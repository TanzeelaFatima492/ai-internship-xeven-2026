from pathlib import Path
import json

import faiss

INDEX_PATH = Path("data/faiss")

INDEX_PATH.mkdir(
    parents=True,
    exist_ok=True
)


class IndexManager:

    def __init__(
        self,
        dimension=384
    ):

        print("Initializing IndexManager...")

        self.dimension = dimension

        self.index_file = INDEX_PATH / "restaurant.index"

        self.mapping_file = INDEX_PATH / "mapping.json"

        # Load or create FAISS index
        if self.index_file.exists():

            print("Loading existing FAISS index...")

            self.index = faiss.read_index(
                str(self.index_file)
            )

        else:

            print("Creating new FAISS index...")

            self.index = faiss.IndexFlatL2(
                self.dimension
            )

        # Load or create mapping
        if self.mapping_file.exists():

            with open(self.mapping_file, "r") as f:

                self.mapping = json.load(f)

        else:

            self.mapping = {}

    def save(self):

        faiss.write_index(
            self.index,
            str(self.index_file)
        )

        print("FAISS index saved successfully.")