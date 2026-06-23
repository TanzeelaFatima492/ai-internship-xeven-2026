import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_groq import ChatGroq

load_dotenv()

documents = []

# TEXT FILE
try:
    text_loader = TextLoader("data.txt")
    text_docs = text_loader.load()
    for d in text_docs:
        d.metadata.update({
            "source_type": "text",
            "domain": "local",
            "date": str(datetime.today().date())
        })
    documents.extend(text_docs)
except Exception as e:
    print("Text file error:", e)

#PDF FILE
try:
    pdf_loader = PyPDFLoader("sample.pdf")
    pdf_docs = pdf_loader.load()
    for d in pdf_docs:
        d.metadata.update({
            "source_type": "pdf",
            "domain": "document",
            "date": str(datetime.today().date())
        })
    documents.extend(pdf_docs)
except Exception as e:
    print("PDF error:", e)

#WEBSITE
try:
    url_loader = WebBaseLoader("https://en.wikipedia.org/wiki/Artificial_intelligence")
    web_docs = url_loader.load()
    for d in web_docs:
        d.metadata.update({
            "source_type": "web",
            "domain": "internet",
            "date": str(datetime.today().date())
        })
    documents.extend(web_docs)
except Exception as e:
    print("Web error:", e)


# 2. SPLIT DOCUMENTS
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)


# 3. EMBEDDINGS + VECTOR STORE
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. FILTERED RETRIEVER
def filtered_search(query, source_type=None, k=3):
    results = vectorstore.similarity_search_with_score(query, k=20)
    filtered = []
    for doc, score in results:
        if source_type:
            if doc.metadata.get("source_type") == source_type:
                filtered.append((doc, score))
        else:
            filtered.append((doc, score))
    return filtered[:k]

# 5. FORMAT CONTEXT + SOURCES
def build_context(results):
    context = ""
    sources = []
    for doc, score in results:
        context += doc.page_content + "\n\n"
        sources.append({
            "source_type": doc.metadata.get("source_type"),
            "domain": doc.metadata.get("domain"),
            "score": float(score)
        })
    return context, sources

# 6. PROMPT (STRICT RAG)
prompt = ChatPromptTemplate.from_template("""
Answer ONLY using the context below.
If answer is missing, say "I don't have that information".

Context:
{context}

Question:
{question}

Answer:
""")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

chain = prompt | llm | StrOutputParser()

# 8. MULTI-DOC RAG PIPELINE
def rag_multi(query, filter_type=None):
    results = filtered_search(query, source_type=filter_type)
    if not results:
        return {"answer": "I don't have that information", "sources": []}
    context, sources = build_context(results)
    answer = chain.invoke({"context": context, "question": query})
    return {"answer": answer, "sources": sources}


# 9. TEST CASES
print("\nTEST 1: Normal Query")
print(rag_multi("What is artificial intelligence?"))

print("\nTEST 2: Filter ONLY web")
print(rag_multi("What is AI?", filter_type="web"))

print("\nTEST 3: Filter ONLY PDF")
print(rag_multi("Explain AI", filter_type="pdf"))