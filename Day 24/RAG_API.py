from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Fake RAG System

class SimpleRAG:
    def __init__(self):
        self.data = {
            "fastapi": "FastAPI is a modern Python web framework.",
            "rag": "RAG combines retrieval + generation using LLMs.",
            "python": "Python is a programming language."
        }

    def retrieve(self, question: str):
        results = []
        for key, value in self.data.items():
            if key in question.lower():
                results.append(value)

        return results

    def generate(self, question: str, context: list):
        if not context:
            return None, None

        answer = f"Based on context: {context[0]}"
        sources = context
        confidence = 0.85

        return answer, sources, confidence


rag_system = None

# Startup Event 

@app.on_event("startup")
def load_rag():
    global rag_system
    rag_system = SimpleRAG()
    print("RAG system loaded successfully!")

# Request Model

class QuestionRequest(BaseModel):
    question: str

# POST /ask Endpoint

@app.post("/ask")
def ask_question(req: QuestionRequest):

    try:
        # Input validation
        if not req.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Step 1: Retrieve
        context = rag_system.retrieve(req.question)

        if not context:
            raise HTTPException(status_code=404, detail="No relevant documents found")

        # Step 2: Generate
        answer, sources, confidence = rag_system.generate(req.question, context)

        if answer is None:
            raise HTTPException(status_code=500, detail="LLM generation failed")

        # Step 3: Return response
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))