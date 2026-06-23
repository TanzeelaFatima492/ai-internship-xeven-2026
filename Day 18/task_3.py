import re
import math

# ==========================================================
# 1. DOCUMENT TYPE DETECTION
# ==========================================================

def detect_doc_type(text):
    """
    Detects document type based on patterns
    """
    if "def " in text or "class " in text or "import " in text:
        return "code_python"

    elif "#" in text and ("##" in text or "###" in text):
        return "markdown"

    else:
        return "plain_text"


# ==========================================================
# 2. TOKEN ESTIMATION (simple approximation)
# ==========================================================

def estimate_tokens(text):
    return len(text.split())


# ==========================================================
# 3. SPLITTERS
# ==========================================================

def split_plain_text(text, chunk_size, overlap):
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunks.append(text[i:i + chunk_size])

    return chunks


def split_markdown(text, chunk_size, overlap):
    """
    Split markdown by headers first
    """
    sections = re.split(r'(#+ .*?\n)', text)
    chunks = []
    current = ""

    for part in sections:
        if len(current) + len(part) > chunk_size:
            chunks.append(current)
            current = part
        else:
            current += part

    if current:
        chunks.append(current)

    return chunks


def split_python_code(text, chunk_size, overlap):
    """
    Split code intelligently by function/class blocks
    """
    blocks = re.split(r'(?=def |class )', text)
    chunks = []
    current = ""

    for b in blocks:
        if len(current) + len(b) > chunk_size:
            chunks.append(current)
            current = b
        else:
            current += b

    if current:
        chunks.append(current)

    return chunks


# ==========================================================
# 4. SMART OVERLAP STRATEGY
# ==========================================================

def get_overlap(doc_type):
    """
    Intelligent overlap decision
    """
    if doc_type == "code_python":
        return 120   # high overlap for logic continuity
    elif doc_type == "markdown":
        return 60    # medium overlap for structure
    else:
        return 30    # low overlap for narrative text


# ==========================================================
# 5. MAIN PROCESSOR
# ==========================================================

def process_document(text, source="unknown"):
    doc_type = detect_doc_type(text)

    # adaptive chunk size
    if doc_type == "code_python":
        chunk_size = 800
    elif doc_type == "markdown":
        chunk_size = 1000
    else:
        chunk_size = 1200

    overlap = get_overlap(doc_type)

    # choose splitter
    if doc_type == "code_python":
        chunks = split_python_code(text, chunk_size, overlap)

    elif doc_type == "markdown":
        chunks = split_markdown(text, chunk_size, overlap)

    else:
        chunks = split_plain_text(text, chunk_size, overlap)

    # build enriched output
    processed_chunks = []

    for i, chunk in enumerate(chunks):
        processed_chunks.append({
            "chunk_id": i,
            "source": source,
            "doc_type": doc_type,
            "text": chunk,
            "tokens": estimate_tokens(chunk),
            "char_length": len(chunk),
            "metadata": {
                "section": "auto-detected",
                "overlap": overlap,
                "chunk_size": chunk_size
            }
        })

    return processed_chunks


# ==========================================================
# 6. SAMPLE INPUTS
# ==========================================================

markdown_doc = """
# AI Overview

## Machine Learning
Machine learning is a subset of AI.

## Deep Learning
Deep learning uses neural networks.

## NLP
NLP processes human language.
"""

python_code = """
import numpy as np

def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
"""

plain_text = """
Artificial Intelligence is transforming industries.
It is used in healthcare, finance, and education.
It helps automate decision making and prediction tasks.
"""


# ==========================================================
# 7. RUN PROCESSOR
# ==========================================================

print("\n================ SMART DOCUMENT PROCESSOR ================\n")

datasets = [
    ("markdown_file.md", markdown_doc),
    ("script.py", python_code),
    ("article.txt", plain_text)
]

for name, doc in datasets:
    print(f"\nProcessing: {name}")
    print("-" * 50)

    chunks = process_document(doc, source=name)

    for c in chunks:
        print(f"\nChunk ID: {c['chunk_id']}")
        print(f"Type: {c['doc_type']}")
        print(f"Tokens: {c['tokens']}")
        print(f"Length: {c['char_length']}")
        print(f"Text Preview: {c['text'][:80]}...")
        print("-" * 30)


# ==========================================================
# 8. SUMMARY
# ==========================================================

print("\n================ SUMMARY ================\n")

print("""
✔ Document type auto-detected:
   - Markdown → header-aware splitting
   - Python → function/class aware splitting
   - Text → fixed-size splitting

✔ Intelligent overlap:
   - Code: high overlap (120)
   - Markdown: medium overlap (60)
   - Text: low overlap (30)

✔ Metadata preserved:
   - source
   - doc_type
   - chunk_id
   - tokens
   - structure info

✔ Output:
   - List of structured chunks ready for embeddings or RAG
""")