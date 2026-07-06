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

        self.dimension = dimension

        self.index_file = INDEX_PATH / "restaurant.index"

        self.mapping_file = INDEX_PATH / "mapping.json"