# 🍽️ Grand Dastarkhwan - AI Menu Assistant (RAG)

AI-powered restaurant menu Q&A system built with FastAPI, FAISS, and Ollama.

## 🚀 Features

- 📄 **PDF Menu Upload** — Upload restaurant menu PDFs
- 🔍 **Smart Search** — Ask questions about menu items in natural language
- 🤖 **AI Answers** — Local LLM (Ollama) generates accurate responses with prices
- 💬 **Conversation Threading** — Group related Q&A into threads
- 📊 **Analytics Dashboard** — Track queries, popular questions, daily usage
- 🧠 **RAG Pipeline** — Retrieval-Augmented Generation for accurate answers

## 🏗️ Architecture

```
PDF Upload → Extract Text → Chunk (500 chars) → Embed (384 dims) → FAISS Vector DB
                                                                        ↓
User Question → Embed → FAISS Search → Retrieve Chunks → Ollama LLM → Answer
                                                                        ↓
                                                              Save to Thread + Analytics
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI + Python 3.14 |
| Database | PostgreSQL + SQLAlchemy |
| Vector DB | FAISS |
| Embeddings | SentenceTransformer (all-MiniLM-L6-v2) |
| LLM | Ollama (llama3.2:1b) — local, FREE |
| Text Splitting | LangChain |
| Testing | Pytest |

## 📦 Installation

### 1. Clone & Setup
```bash
git clone <repo-url>
cd "Day 27/Full Stack RAG"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Create PostgreSQL database
createdb FullStack_rag

# Configure .env
echo DATABASE_URL=postgresql://postgres:12345@localhost:5432/FullStack_rag > .env
echo SECRET_KEY=mysecretkey123 >> .env
echo ALGORITHM=HS256 >> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=60 >> .env
```

### 3. Install Ollama (for AI answers)
```bash
# Download from https://ollama.com/download/windows
ollama pull llama3.2:1b
```

### 4. Run Server
```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs

## 📡 API Endpoints

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents/upload` | Upload PDF menu |

### RAG Query
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rag/query` | Ask question, get AI answer |
| GET | `/rag/threads` | List conversation threads |
| GET | `/rag/threads/{id}` | Get thread history |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/overview` | System stats |
| GET | `/analytics/popular-questions` | Most asked questions |
| GET | `/analytics/recent-queries` | Recent activity |
| GET | `/analytics/daily-usage` | Queries per day |

## 🧪 Usage Example

```bash
# Upload menu
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@sample.pdf"

# Ask question
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the price of Chicken Karahi?", "top_k": 3}'

# Response
{
  "question": "What is the price of Chicken Karahi?",
  "answer": "The price of Chicken Karahi is Rs 2,400 (Full).",
  "sources": [...]
}
```

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

## 📂 Project Structure

```
Full Stack RAG/
├── app/
│   ├── api/           # API endpoints
│   │   ├── rag.py        # Query & threads
│   │   └── analytics.py  # Analytics dashboard
│   ├── services/      # Business logic
│   │   ├── embedding_service.py
│   │   ├── faiss_store.py
│   │   ├── llm.py
│   │   ├── pdf_service.py
│   │   └── chunk_service.py
│   ├── models/        # SQLAlchemy models
│   ├── database/      # DB config
│   └── main.py
├── tests/             # Unit tests
├── data/
│   ├── uploads/       # PDF files
│   └── faiss_index/   # Vector storage
└── .env               # Environment variables
```

## 👩‍💻 Author

Tanzeela Fatima — AI Internship 2026