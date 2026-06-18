from pydantic import BaseModel
from typing import List
from datetime import date

# 🔑 Import config (loads API key automatically)
import config

from langchain_openai import ChatOpenAI

# 📦 Pydantic Model
class Article(BaseModel):
    title: str
    author: str
    published_date: date
    summary: str
    tags: List[str]


# 🤖 LLM Setup
llm = ChatOpenAI(model="gpt-4o-mini")

article_chain = llm.with_structured_output(Article)


# 🧾 Input Text
raw_text = """
Title: AI Revolution in 2026
Author: John Smith
Published Date: 2026-06-10
Summary: AI is transforming industries rapidly.
Tags: AI, technology, future
"""


# 🚀 Run Pipeline
def safe_parse(text):
    try:
        return article_chain.invoke(text)
    except Exception as e:
        print("Error:", e)

        return Article(
            title="Unknown",
            author="Unknown",
            published_date="2026-01-01",
            summary="Parsing failed",
            tags=[]
        )


result = safe_parse(raw_text)

print("\n📌 Structured Output:\n")
print(result)

print("\n📊 JSON Format:\n")
print(result.model_dump())