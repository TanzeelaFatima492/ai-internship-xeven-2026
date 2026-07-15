# 🤖 Pulse Chat — AI Chatbot with Multi-Conversation Support

A full-stack AI chatbot application built with **FastAPI**, **Next.js**, **PostgreSQL**, and **Groq AI**.
Supports multiple users, JWT authentication, conversation memory, and ChatGPT-style multi-conversation sidebar.

---

## 🚀 Features

- 🔐 **User Authentication** — Signup, Login, JWT token-based auth
- 💬 **AI Chatbot** — Real AI responses via Groq API (Llama 3.1)
- 🧠 **Conversation Memory** — Bot remembers context within a conversation
- 📂 **Multi-Conversation Sidebar** — Separate chats like ChatGPT
- 🔄 **Persistent History** — Messages survive page refresh
- 👤 **User Isolation** — Each user sees only their own chats
- 🎨 **Modern UI** — Dark/Light mode, responsive design
- 🗄️ **PostgreSQL Database** — All conversations stored permanently

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, Tailwind CSS, TypeScript |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| AI Model | Groq API (Llama 3.1 8B) |
| Auth | JWT (JSON Web Tokens) |
| UI | v0.vercel generated components |

---

## 📁 Project Structure

```
User Authentication & Chatbot API/
├── app/
│   ├── routers/
│   │   ├── auth.py          # Auth endpoints
│   │   └── chat.py          # Chat endpoints
│   ├── services/
│   │   └── chatbot.py       # AI service (Groq)
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB connection
│   └── utils/
│       └── token.py         # JWT helpers
├── main.py                  # FastAPI entry point
├── requirements.txt
├── .env                     # API keys
│
├── Chatbot_frontend/        # Next.js frontend
│   ├── components/
│   │   ├── chat-view.tsx    # Main chat view
│   │   ├── chat-sidebar.tsx # Sidebar
│   │   ├── chat-messages.tsx # Message display
│   │   └── message-input.tsx # Input box
│   └── lib/
│       └── api.ts           # API client
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd "User Authentication & Chatbot API"
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=gsk_your_key_here
DATABASE_URL=postgresql://postgres:12345@localhost/chatbot_db
SECRET_KEY=mysecretkey" > .env

# Start backend
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd Chatbot_frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local

# Start frontend
npm run dev
```

### 4. Database Setup

```sql
-- Create database in PostgreSQL
CREATE DATABASE chatbot_db;

-- Tables are auto-created by SQLAlchemy on first run
```

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/signup` | Register new user | No |
| POST | `/login` | Login + get JWT token | No |
| POST | `/chat/` | Send message | Yes |
| GET | `/chat/history` | Get chat history | Yes |

### Chat Request Format

```json
// First message (new conversation)
{
  "query": "Hello!",
  "bot_id": 0
}

// Continue conversation
{
  "query": "What's my name?",
  "bot_id": 405015202625925
}
```

---

## 🎯 How It Works

1. **User signs up** → Account created in PostgreSQL
2. **User logs in** → JWT token generated
3. **First message** → `bot_id: 0` → Backend creates new bot_id
4. **Next messages** → Same `bot_id` continues conversation
5. **New Chat button** → Resets `bot_id: 0` → New conversation
6. **Sidebar** → Shows all conversations grouped by bot_id

---

## 🐛 Known Issues & Fixes

| Issue | Solution |
|-------|----------|
| Conversations merge after refresh | `api.ts` — add `bot_id` to `ChatMessage` type |
| "I'm having trouble" error | Check `.env` — `GROQ_API_KEY` must be valid |
| `psycopg2` error on Python 3.14 | Use `pg8000` or downgrade to Python 3.12 |
| Sidebar shows only 1 conversation | Ensure `getHistory` returns `bot_id` field |

---

## 📝 Commit History

```
fix: group conversations by bot_id in sidebar and history API
fix: persist bot_id in localStorage for conversation continuity
fix: bot response display and bot_id in database
fix: use user-specific bot_id for conversation isolation
feat: add multi-tool ReAct agent with memory and performance tracking
feat: implement full User Authentication & Chatbot API
```

---

## 👩‍💻 Author

**Tanzeela Fatima**
AI Engineer Intern
Xeven Solutions

---

## 📄 License

This project is for internship training purposes.