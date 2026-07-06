import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = "deepseek/deepseek-r1:free"
            print("✅ OpenRouter FREE ready")
        else:
            print("⚠️ No key — fallback mode")
    
    def generate_answer(self, question, context_chunks):
        if not self.api_key:
            return self._fallback(question, context_chunks)
        
        context_text = "\n\n".join([f"[{i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)])
        
        prompt = f"""Answer ONLY from this menu. Be specific, include prices.

MENU:
{context_text}

QUESTION: {question}

ANSWER:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return self._fallback(question, context_chunks)
    
    def _fallback(self, question, context_chunks):
        return "📋 Found:\n\n" + "\n---\n".join(context_chunks[:3])

llm_service = LLMService()