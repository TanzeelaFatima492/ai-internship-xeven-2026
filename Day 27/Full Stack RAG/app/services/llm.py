import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GROK_API_KEY")
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
            self.model = "grok-2-latest"
            print("✅ Grok AI ready")
        else:
            print("⚠️ No Grok API key found — using fallback mode")
    
    def generate_answer(self, question, context_chunks):
        if not self.api_key:
            return self._fallback(question, context_chunks)
        
        context_text = "\n\n".join([
            f"[Source {i+1}]:\n{chunk}" 
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a helpful restaurant assistant. Answer based ONLY on the menu below.
If not in the menu, say "I don't have this information in the menu."

MENU CONTEXT:
{context_text}

CUSTOMER QUESTION: {question}

ANSWER (be specific, include prices):"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise restaurant assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Grok error: {e}")
            return self._fallback(question, context_chunks)
    
    def _fallback(self, question, context_chunks):
        return f"📋 Found these relevant menu items:\n\n" + "\n---\n".join(context_chunks[:3])

llm_service = LLMService()