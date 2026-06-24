import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Load API key from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question: str, context: str):
    """
    RAG LLM function:
    - Takes question
    - Takes retrieved context
    - Sends both to Groq LLM
    - Returns final answer
    """

    prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer the question.
If answer is not in context, say "I don't know".

------------------
Context:
{context}
------------------

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content