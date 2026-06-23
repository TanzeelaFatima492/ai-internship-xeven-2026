import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#   Pinecone client init  
pc = Pinecone(api_key=PINECONE_API_KEY)
EMBED_MODEL = "multilingual-e5-large"

#   Document loading  
loader = TextLoader("data.txt", encoding="utf-8")
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

#   Embed function using Pinecone Inference  
def embed(texts):
    if isinstance(texts, str):
        texts = [texts]
    result = pc.inference.embed(
        model=EMBED_MODEL,
        inputs=texts,
        parameters={"input_type": "passage"}
    )
    return [d.values for d in result.data]

#   Create/Reset index  
index_name = "rag-index"
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

pc.create_index(
    name=index_name,
    dimension=1024,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
index = pc.Index(index_name)

#   Upsert vectors  
vectors = []
for i, doc in enumerate(docs):
    emb = embed(doc.page_content)[0]
    vectors.append((str(i), emb, {"text": doc.page_content}))
index.upsert(vectors=vectors)

#   Retrieval  
def retrieve(query, k=4):
    q_emb = embed([query])[0]
    res = index.query(vector=q_emb, top_k=k, include_metadata=True)
    return [match["metadata"]["text"] for match in res["matches"]]

#   LLM & Prompt (same)  
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful assistant. Use ONLY the context below. If answer is not in context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:"""
)

def ask(query: str):
    context_docs = retrieve(query)
    context = "\n\n".join(context_docs)
    final_prompt = prompt.format(context=context, question=query)
    response = llm.invoke(final_prompt)
    print("\nANSWER:\n", response.content)
    print("\nSOURCES:\n")
    for i, doc in enumerate(context_docs, 1):
        print(f"\nSource {i}:\n{doc[:300]}")

if __name__ == "__main__":
    ask("What is RAG?")