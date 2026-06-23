import os
import json
import uuid

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    FAISS_PATH,
    UPLOAD_PATH
)


class DocumentManager:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        self.metadata_file = os.path.join(
            FAISS_PATH,
            "metadata.json"
        )

        os.makedirs(UPLOAD_PATH, exist_ok=True)
        os.makedirs(FAISS_PATH, exist_ok=True)

        self._initialize_metadata()

    def _initialize_metadata(self):

        if not os.path.exists(self.metadata_file):

            with open(self.metadata_file, "w") as f:
                json.dump({"documents": []}, f)

    def _load_metadata(self):

        with open(self.metadata_file, "r") as f:
            return json.load(f)

    def _save_metadata(self, data):

        with open(self.metadata_file, "w") as f:
            json.dump(data, f, indent=4)

    def _load_document(self, filepath):

        if filepath.endswith(".pdf"):
            loader = PyPDFLoader(filepath)

        elif filepath.endswith(".txt"):
            loader = TextLoader(filepath)

        else:
            raise ValueError(
                "Only PDF and TXT files are supported"
            )

        return loader.load()

    def _chunk_document(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        return splitter.split_documents(documents)

    def upload_document(self, filepath, filename):

        document_id = str(uuid.uuid4())

        docs = self._load_document(filepath)

        chunks = self._chunk_document(docs)

        for chunk in chunks:

            chunk.metadata["document_id"] = document_id

            chunk.metadata["filename"] = filename

        index_path = os.path.join(
            FAISS_PATH,
            "index"
        )

        if os.path.exists(index_path):

            vectorstore = FAISS.load_local(
                index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )

            vectorstore.add_documents(chunks)

        else:

            vectorstore = FAISS.from_documents(
                chunks,
                self.embeddings
            )

        vectorstore.save_local(index_path)

        metadata = self._load_metadata()

        metadata["documents"].append(
            {
                "id": document_id,
                "filename": filename,
                "chunks": len(chunks)
            }
        )

        self._save_metadata(metadata)

        return {
            "document_id": document_id,
            "filename": filename,
            "chunks": len(chunks),
            "status": "indexed"
        }

    def list_documents(self):

        metadata = self._load_metadata()

        return metadata["documents"]