import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Hamein parameter effects ko observe karne ke liye ek stable free model chahiye
MODEL_NAME = "meta-llama/llama-3.3-70b-instruct:free"

def run_experiment(prompt, temp=0.7, max_tok=100, top_p=1.0):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=max_tok,
            top_p=top_p
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

#Expirement 1
prompt_temp = "Finish this phrase with a unique creative twist: 'The old clock on the wall...'"
print("--- EXPERIMENT 1: TEMPERATURE ---")
print(f"[Temp 0.0 (Deterministic)]:\n{run_experiment(prompt_temp, temp=0.0)}")
print(f"\n[Temp 0.7 (Balanced)]:\n{run_experiment(prompt_temp, temp=0.7)}")
print(f"\n[Temp 1.5 (Creative/Wild)]:\n{run_experiment(prompt_temp, temp=1.5)}")

# EXPERIMENT 2: Max Tokens Truncation
prompt_tokens = "Write a comprehensive 3-paragraph story about a spaceship."
print("\n--- EXPERIMENT 2: MAX TOKENS TRUNCATION ---")
print(f"[Max Tokens = 15]:\n{run_experiment(prompt_tokens, max_tok=15)}")
print(f"\n[Max Tokens = 60]:\n{run_experiment(prompt_tokens, max_tok=60)}")

#3: Top_P Sampling

prompt_top_p = "Name a rare and exotic flavor of ice cream."
print("\n--- EXPERIMENT 3: TOP_P SAMPLING ---")
print(f"[Top_P 0.1 (Highly Focused)]:\n{run_experiment(prompt_top_p, top_p=0.1, temp=1.0)}")
print(f"\n[Top_P 0.9 (Diverse/Unexpected)]:\n{run_experiment(prompt_top_p, top_p=0.9, temp=1.0)}")