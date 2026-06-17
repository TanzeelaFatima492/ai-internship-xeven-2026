# Document Chunking in AI

## Why Chunking is Important
Chunking helps large documents fit into LLM context limits and improves retrieval accuracy in RAG systems.

## Chunking Strategies
We use fixed size, sentence-based, and semantic chunking depending on the use case.

## LangChain Splitters
RecursiveCharacterTextSplitter is widely used for general documents, while MarkdownHeaderTextSplitter is best for structured markdown files.

## Metadata Preservation
Each chunk should store source, page number, and section headers for better traceability.

## Trade-offs
Small chunks give high precision but low context, while large chunks give more context but lower precision.