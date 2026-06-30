from pydantic import BaseModel
from typing import List
from datetime import date
from dotenv import load_dotenv
from langchain_groq import ChatGroq

import os
import json

#   ---
# Load Environment
#   ---

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

#   ---
# Pydantic Model
#   ---

class Article(BaseModel):
    title: str
    author: str
    published_date: date
    summary: str
    tags: List[str]

#   ---
# LLM
#   ---

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key,
)

#   ---
# Raw Article
#   ---

raw_text = """
Title: AI Revolution in 2026

Author: John Smith

Published Date: 2026-06-10

Summary:
AI is transforming industries rapidly through automation,
machine learning, and large language models.

Tags:
AI, technology, future
"""

#   ---
# Prompt
#   ---

prompt = f"""
Extract the following article information.

Return ONLY valid JSON.

Required format:

{{
    "title":"",
    "author":"",
    "published_date":"",
    "summary":"",
    "tags":[]
}}

Article:

{raw_text}
"""

#   ---
# Safe Parse
#   ---

def safe_parse():

    try:

        response = llm.invoke(prompt)

        text = response.content.strip()

        print("\nRaw LLM Output:\n")
        print(text)

        data = json.loads(text)

        article = Article(**data)

        return article

    except Exception as e:

        print("\nError:", e)

        return Article(
            title="Unknown",
            author="Unknown",
            published_date="2026-01-01",
            summary="Parsing failed",
            tags=[]
        )

#   ---
# Run
#   ---

result = safe_parse()

print("\nStructured Output:\n")
print(result)

print("\nJSON Format:\n")
print(result.model_dump())