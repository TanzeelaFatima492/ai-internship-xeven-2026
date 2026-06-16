import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Client initialize karte waqt OpenRouter ka base_url dena zaroori hai
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_completion(prompt, temp=0.7):
    response = client.chat.completions.create(
        # Yahan OpenRouter par supported model slug use kar rahe hain
        model="deepseek/deepseek-r1",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        max_tokens=150
    )
    
    content = response.choices[0].message.content
    tokens = response.usage
    
    return content, tokens

# Task: Simple prompt and observe usage
prompt = "Explain LLMs in one sentence."
result, usage = get_completion(prompt, temp=0.7)

print(f"--- Response ---\n{result}\n")
print(f"--- Token Usage ---")
print(f"Prompt Tokens: {usage.prompt_tokens}")
print(f"Completion Tokens: {usage.completion_tokens}")
print(f"Total Tokens: {usage.total_tokens}")