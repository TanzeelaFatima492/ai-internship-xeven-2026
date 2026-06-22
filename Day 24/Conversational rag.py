import os
import json
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# LOAD ENV

load_dotenv()

# CHAT HISTORY (JSON)

CHAT_FILE = "chat_history.json"

def load_history():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(CHAT_FILE, "w") as f:
        json.dump(data, f, indent=4)

chat_store = load_history()

# LOAD DOCUMENTS

loader = TextLoader("data.txt", encoding="utf-8")
documents = loader.load()

texts = [d.page_content for d in documents if d.page_content.strip()]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.create_documents(texts)

print("📦 Total chunks:", len(docs))

# EMBEDDINGS + VECTOR DB

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# GUIDE MESSAGE

print("""
💡 HOW TO ASK QUESTIONS:
 Only ask questions related to FAISS, Chroma, vector databases.
""")

# CHECK RELEVANCE

def is_relevant(query, docs):
    content = " ".join([d.page_content.lower() for d in docs])

    for word in query.lower().split():
        if word in content:
            return True

    return False

# CHAT FUNCTION

def chat(user_id, query):

    history = chat_store.get(user_id, [])

    context_docs = retriever.invoke(query)
    context = "\n".join([d.page_content for d in context_docs])

    #  OUT OF CONTEXT HANDLING
    if len(query.strip()) < 3:
        return " Please ask a proper question (e.g. What is FAISS?)"

    if not is_relevant(query, context_docs):
        answer = " I don't have that information in my knowledge base. Please ask related questions about FAISS, Chroma, or vector databases."
    else:
        answer = f"""
🤖 AI ANSWER:

{context[:500]}
"""

    # save history
    history.append(f"User: {query}")
    history.append(f"AI: {answer}")

    chat_store[user_id] = history[-20:]
    save_history(chat_store)

    return answer


# CHAT LOOP

print("\n💬 Conversational RAG Chatbot Started\n")

user_id = input("👤 Enter your name: ")

while True:

    print("\n Recent Chat:")
    for msg in chat_store.get(user_id, [])[-6:]:
        print(msg)

    query = input("\n 👱:")

    if query.lower() == "exit":
        print("👋 Chat Ended")
        break

    answer = chat(user_id, query)

    print("\n🤖", answer)