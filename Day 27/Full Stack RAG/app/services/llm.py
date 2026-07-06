import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.use_openai = False
        
        if self.api_key and self.api_key != "your-openai-api-key-here":
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            self.use_openai = True
            print("✅ OpenAI ready")
        else:
            print("⚠️ No OpenAI key found — using fallback mode")
    
    def generate_answer(self, question, context_chunks):
        """Generate answer using retrieved chunks as context"""
        
        if self.use_openai:
            return self._openai_answer(question, context_chunks)
        else:
            return self._fallback(question, context_chunks)
    
    def _openai_answer(self, question, context_chunks):
        """Use OpenAI to generate answer"""
        context_text = "\n\n".join([
            f"[Source {i+1}]:\n{chunk}" 
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a helpful restaurant assistant. Answer the question based ONLY on the menu information provided below.
If the answer is not in the context, say "I don't have this information in the menu."

MENU CONTEXT:
{context_text}

CUSTOMER QUESTION: {question}

ANSWER (be specific, include prices when available):"""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a precise restaurant assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content
    
    def _fallback(self, question, context_chunks):
        """Fallback — return relevant chunks directly"""
        return f"📋 Found these relevant menu items:\n\n" + "\n---\n".join(context_chunks[:3])

# Global instance
llm_service = LLMService()