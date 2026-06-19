import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
index = None

def rebuild_index():
    global index

    if len(documents) == 0:
        index = None
        return

    embeddings = model.encode(documents)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

# Add Document
def add_document():
    text = input("Enter document: ")

    documents.append(text)
    rebuild_index()

    print("Document added successfully!")


# Show Documents
def show_documents():
    if len(documents) == 0:
        print("No documents available.")
        return

    print("\nStored Documents:\n")

    for i, doc in enumerate(documents):
        print(f"{i+1}. {doc}")


# Delete Document
def delete_document():
    show_documents()

    if len(documents) == 0:
        return

    try:
        choice = int(input("\nEnter document number to delete: "))

        if 1 <= choice <= len(documents):
            removed = documents.pop(choice - 1)
            rebuild_index()
            print(f"Deleted: {removed}")

        else:
            print("Invalid choice.")

    except:
        print("Invalid input.")


# Search
def search_documents():
    if index is None:
        print("No documents stored.")
        return

    query = input("Enter query: ")

    k = int(input("Enter K: "))

    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype("float32")

    distances, indices = index.search(
        query_vector,
        min(k, len(documents))
    )

    print("\nTop Results:\n")

    for rank, idx in enumerate(indices[0]):
        print(f"Rank {rank+1}")
        print("Document:", documents[idx])
        print("Distance:", distances[0][rank])
        print()


# Save
def save_data():

    with open("documents.pkl", "wb") as f:
        pickle.dump(documents, f)

    if index is not None:
        faiss.write_index(index, "faiss.index")

    print("Data saved.")

# Load
def load_data():

    global documents
    global index

    try:
        with open("documents.pkl", "rb") as f:
            documents = pickle.load(f)

        index = faiss.read_index("faiss.index")

        print("Data loaded.")

    except:
        print("No saved data found.")

while True:

    print("\n")
    print("=" * 40)
    print("      FAISS VECTOR DATABASE")
    print("=" * 40)

    print("1. Add Document")
    print("2. Search Documents")
    print("3. Delete Document")
    print("4. Show Documents")
    print("5. Save Data")
    print("6. Load Data")
    print("7. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        add_document()

    elif choice == "2":
        search_documents()

    elif choice == "3":
        delete_document()

    elif choice == "4":
        show_documents()

    elif choice == "5":
        save_data()

    elif choice == "6":
        load_data()

    elif choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")