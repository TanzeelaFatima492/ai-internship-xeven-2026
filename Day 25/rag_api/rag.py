import uuid

documents = {}
vector_store = []  # simple in-memory placeholder

def add_document(text, filename):
    doc_id = str(uuid.uuid4())

    chunks = text.split("\n\n")

    documents[doc_id] = {
        "filename": filename,
        "chunks": chunks,
    }

    return doc_id, len(chunks)


def search_documents(query, top_k=5):
    results = []

    for doc_id, doc in documents.items():
        for chunk in doc["chunks"]:
            if query.lower() in chunk.lower():
                results.append({
                    "text": chunk,
                    "source": doc["filename"]
                })

    return results[:top_k]