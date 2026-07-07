import ollama

class LLMService:
    def __init__(self):
        self.model = "llama3.2:1b"
        print("✅ Ollama LLM ready (local, FREE)")
    
    def generate_answer(self, question, context_chunks):
        context_text = "\n\n".join([f"[{i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)])
        
        prompt = f"""You are a restaurant assistant. Answer ONLY from this menu. Be specific, include prices.

MENU:
{context_text}

QUESTION: {question}

ANSWER:"""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={"temperature": 0.3, "num_predict": 150}
            )
            return response["response"].strip()
        except Exception as e:
            print(f"⚠️ Ollama error: {e}")
            return self._fallback(question, context_chunks)
    
    def _fallback(self, question, context_chunks):
        return "📋 Found:\n\n" + "\n---\n".join(context_chunks[:3])

llm_service = LLMService()