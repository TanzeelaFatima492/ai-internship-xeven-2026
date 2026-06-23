"""
==========================================================
Document Chunking in LangChain - Complete Example
==========================================================

Topics Covered:
1. Context Preservation
2. RecursiveCharacterTextSplitter
3. TokenTextSplitter
4. MarkdownHeaderTextSplitter
5. Metadata Preservation
6. Small vs Large Chunk Trade-offs

Install:
pip install langchain langchain-text-splitters tiktoken
"""

# ==========================
# Sample Document
# ==========================

text = """
Artificial Intelligence (AI) is a branch of computer science.

Machine Learning (ML) is a subset of AI.
It enables computers to learn from data.

Deep Learning is a subset of Machine Learning.
It uses neural networks with many layers.

Natural Language Processing (NLP) helps computers understand human language.

Computer Vision allows machines to interpret images and videos.

AI has applications in healthcare, finance, education, robotics, and many other fields.
"""

# ==========================================================
# 1. Context Preservation using RecursiveCharacterTextSplitter
# ==========================================================

print("=" * 60)
print("1. RecursiveCharacterTextSplitter")
print("=" * 60)

from langchain_text_splitters import RecursiveCharacterTextSplitter

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

recursive_chunks = recursive_splitter.split_text(text)

for i, chunk in enumerate(recursive_chunks):
    print(f"\nChunk {i+1}")
    print(chunk)

# ==========================================================
# 2. TokenTextSplitter
# ==========================================================

print("\n")
print("=" * 60)
print("2. TokenTextSplitter")
print("=" * 60)

from langchain_text_splitters import TokenTextSplitter

token_splitter = TokenTextSplitter(
    chunk_size=30,
    chunk_overlap=5
)

token_chunks = token_splitter.split_text(text)

for i, chunk in enumerate(token_chunks):
    print(f"\nToken Chunk {i+1}")
    print(chunk)

# ==========================================================
# 3. MarkdownHeaderTextSplitter
# ==========================================================

print("\n")
print("=" * 60)
print("3. MarkdownHeaderTextSplitter")
print("=" * 60)

markdown_text = """
# Artificial Intelligence

## Machine Learning

Machine Learning is a subset of AI.

## Deep Learning

Deep Learning uses neural networks.

## NLP

Natural Language Processing works with text.
"""

from langchain_text_splitters import MarkdownHeaderTextSplitter

headers = [
    ("#", "Title"),
    ("##", "Section"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers
)

md_docs = markdown_splitter.split_text(markdown_text)

for i, doc in enumerate(md_docs):
    print(f"\nMarkdown Chunk {i+1}")
    print(doc.page_content)
    print("Metadata:", doc.metadata)

# ==========================================================
# 4. Metadata Preservation
# ==========================================================

print("\n")
print("=" * 60)
print("4. Metadata Preservation")
print("=" * 60)

from langchain_core.documents import Document

documents = [
    Document(
        page_content="Machine Learning is a subset of AI.",
        metadata={
            "source": "AI_Book.pdf",
            "page": 12,
            "section": "Introduction"
        }
    ),
    Document(
        page_content="Deep Learning uses neural networks.",
        metadata={
            "source": "AI_Book.pdf",
            "page": 18,
            "section": "Deep Learning"
        }
    )
]

for doc in documents:
    print("\nContent:")
    print(doc.page_content)
    print("Metadata:")
    print(doc.metadata)

# ==========================================================
# 5. Small vs Large Chunk Trade-offs
# ==========================================================

print("\n")
print("=" * 60)
print("5. Small vs Large Chunk Comparison")
print("=" * 60)

small_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)

large_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20
)

small_chunks = small_splitter.split_text(text)
large_chunks = large_splitter.split_text(text)

print("\nSmall Chunks")
print("-" * 30)

for i, chunk in enumerate(small_chunks):
    print(f"\nSmall Chunk {i+1}")
    print(chunk)

print("\n")
print("Large Chunks")
print("-" * 30)

for i, chunk in enumerate(large_chunks):
    print(f"\nLarge Chunk {i+1}")
    print(chunk)

# ==========================================================
# 6. Summary
# ==========================================================

print("\n")
print("=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
1. Context Preservation:
   - Uses chunk overlap to avoid losing information.

2. RecursiveCharacterTextSplitter:
   - Splits by paragraphs, lines, spaces, then characters.
   - Best general-purpose splitter.

3. TokenTextSplitter:
   - Splits by token count.
   - Ideal for embedding models and LLMs.

4. MarkdownHeaderTextSplitter:
   - Splits markdown documents by headings.
   - Preserves document structure.

5. Metadata Preservation:
   - Stores source, page number, and section information.
   - Helps with citations and retrieval.

6. Chunk Size Trade-offs:

   Small Chunks:
   + High precision
   + Fast retrieval
   - Less context

   Large Chunks:
   + More context
   + Better for long topics
   - Lower precision

Best Practice:
Use RecursiveCharacterTextSplitter
Chunk Size: 512 tokens
Chunk Overlap: 50-100 tokens
Preserve metadata with every chunk.
""")

print("=" * 60)
print("Program Completed Successfully!")
print("=" * 60)