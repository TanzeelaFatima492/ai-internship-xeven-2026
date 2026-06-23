import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

from config import (
    EMBEDDING_MODEL,
    FAISS_PATH,
    TOP_K
)


class RAGService:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        self.index_path = os.path.join(
            FAISS_PATH,
            "index"
        )

        self.vectorstore = None

        self.load_index()

    def load_index(self):

        if os.path.exists(self.index_path):

            self.vectorstore = FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )

    def reload_index(self):

        self.load_index()

    def search(self, query):

        if not self.vectorstore:
            return []

        docs = self.vectorstore.similarity_search_with_score(
            query,
            k=TOP_K
        )

        results = []

        for doc, score in docs:

            results.append(
                {
                    "content": doc.page_content,
                    "score": float(score),
                    "source": doc.metadata.get(
                        "filename",
                        "Unknown"
                    )
                }
            )

        return results

    def retrieve_context(self, query):

        if not self.vectorstore:
            return [], ""

        docs = self.vectorstore.similarity_search(
            query,
            k=TOP_K
        )

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        sources = list(
            set(
                doc.metadata.get(
                    "filename",
                    "Unknown"
                )
                for doc in docs
            )
        )

        return sources, context

    def calculate_confidence(self, search_results):

        if not search_results:
            return 0.0

        scores = [
            result["score"]
            for result in search_results
        ]

        avg_score = sum(scores) / len(scores)

        confidence = 1 / (1 + avg_score)

        return round(confidence, 2)

    async def generate_answer(self, question):

        sources, context = self.retrieve_context(
            question
        )

        if not context:

            return {
                "answer": "No relevant information found.",
                "sources": [],
                "confidence": 0.0
            }

        # LLM Integration Later

        answer = f"""
Based on the retrieved documents:

{context[:1000]}
"""

        confidence = self.calculate_confidence(
            self.search(question)
        )

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }