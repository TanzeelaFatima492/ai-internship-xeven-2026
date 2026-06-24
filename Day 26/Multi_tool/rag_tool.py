from langchain_classic.tools import tool

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_vectorstore():

    loader = TextLoader("documents.txt")

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore


vectorstore = build_vectorstore()


@tool
def rag_search(query: str) -> str:
    """
    Search local documents and return relevant information.

    Args:
        query: User question.

    Returns:
        Relevant document content.
    """
    try:
        docs = vectorstore.similarity_search(
            query,
            k=3
        )

        if not docs:
            return "No relevant documents found."

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )

    except Exception as e:
        return f"RAG Error: {str(e)}"


if __name__ == "__main__":
    question = input("Ask question: ")
    print(rag_search.invoke(question))