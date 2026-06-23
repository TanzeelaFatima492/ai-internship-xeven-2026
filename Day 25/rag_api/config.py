from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))

CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

TOP_K = int(os.getenv("TOP_K"))

FAISS_PATH = os.getenv("FAISS_PATH")

UPLOAD_PATH = os.getenv("UPLOAD_PATH")