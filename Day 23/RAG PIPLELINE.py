import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq              # ← Groq instead of Gemini

# ---------- 0. Load API key from .env ----------
load_dotenv()

# ---------- 1. Load & split documents ----------
loader = TextLoader("data.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs = splitter.split_documents(documents)

# ---------- 2. Embeddings & FAISS vector store ----------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.from_documents(docs, embeddings)

# ---------- 3. Retriever ----------
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ---------- 4. Prompt template ----------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Use the provided context to answer the question.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",   # fast, free, current
    temperature=0
)

# ---------- 6. Helper to format retrieved docs ----------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# ---------- 7. LCEL RAG chain ----------
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ---------- 8. Ask a question ----------
query = "What is RAG?"
answer = rag_chain.invoke(query)

print("ANSWER:")
print(answer)

# ---------- 9. Show retrieved sources ----------
retrieved_docs = retriever.invoke(query)
print("\nSOURCES:")
for i, doc in enumerate(retrieved_docs, start=1):
    print(f"\nSource {i}")
    print(doc.page_content[:300])