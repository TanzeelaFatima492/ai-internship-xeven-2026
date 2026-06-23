import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain

# Load API keys
load_dotenv()

#!. Data loading
if not os.path.exists("data.txt"):
    raise FileNotFoundError("data.txt not found – please create it with some content about FAISS, Chroma, etc.")

loader = TextLoader("data.txt", encoding="utf-8")
documents = loader.load()

# keep only non-empty texts
texts = [d.page_content for d in documents if d.page_content.strip()]

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents(texts)
print(f"📦 Total chunks: {len(docs)}")

#2. Embeddings & Vector Store 
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# 4. Memory with SUMMARIZATION
memory = ConversationSummaryBufferMemory(
    llm=llm,                     # same LLM used to summarise old conversations
    memory_key="chat_history",   # chain expects this key
    return_messages=True,
    max_token_limit=300,         # summarise older messages when buffer exceeds this limit
)

#5. Conversational RAG Chain 
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    verbose=False   # set True if you want to see retrieved documents
)

#6. Chat Loop
print("\n💬 Conversational RAG Chatbot (Memory + Summarisation)")
print("Type 'exit' to stop.\n")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Chat ended.")
        break

    result = qa_chain.invoke({"question": query})
    print("Bot:", result["answer"])
    print("-" * 50)