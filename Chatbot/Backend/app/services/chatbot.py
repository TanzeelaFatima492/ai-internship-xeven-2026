import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversations = {}

def get_ai_response(user_message: str, bot_id: str = None, user_id: str = None) -> str:
    try:
        key = f"{user_id}_{bot_id}" if user_id and bot_id else "default"
        
        if key not in conversations:
            conversations[key] = [
                {"role": "system", "content": "You are a helpful assistant. Keep answers short and remember user details like name."}
            ]
        
        messages = conversations[key]
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        
        if len(messages) > 21:
            conversations[key] = [messages[0]] + messages[-20:]
        
        return reply
    except Exception:
        return "Sorry, I couldn't process that."