import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------- 0. Load environment (API token) ----------
load_dotenv()

# ---------- 1. Load documents ----------
loader = TextLoader("data.txt")   # file must be in the same folder
documents = loader.load()

# ---------- 2. Split ----------
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = splitter.split_documents(documents)

# ---------- 3. Embeddings & FAISS vector store ----------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.from_documents(docs, embeddings)

# ---------- 4. Retriever ----------
retriever = vectorstore.as_retriever()

# ---------- 5. Helper to format context ----------
def format_context(docs):
    return "\n\n".join([d.page_content for d in docs])

# ---------- 6. Prompt ----------
prompt = ChatPromptTemplate.from_template("""
Answer ONLY from context.
If answer is not in context, say "I don't have that information".

Context:
{context}

Question:
{question}
""")


llm = ChatGroq(
    model="llama-3.1-8b-instant",   # current free model
    temperature=0,
    # API key read automatically from GROQ_API_KEY in .env
)

# ---------- 8. LCEL chain ----------
chain = prompt | llm | StrOutputParser()

# ---------- 9. RAG function ----------
def rag(question):
    docs = retriever.invoke(question)   
    context = format_context(docs)

    if not context.strip():
        return "I don't have that information"

    return chain.invoke({
        "context": context,
        "question": question
    })

# ---------- 10. Test ----------
print("\nWhat is RAG?")
print(rag("What is RAG?"))
print("\nWhy FAISS ?")
print(rag("What is FAISS?"))
print("\nWhat is quantum teleportation in aliens?")
print(rag("What is quantum teleportation in aliens?"))