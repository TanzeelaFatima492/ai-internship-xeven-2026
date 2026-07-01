# 🚀 AI Engineer Internship Project - Xeven Solutions

## 📌 Project Title
User Authentication & Chatbot API using FastAPI + PostgreSQL

---

## 📖 About the Internship

This project is part of my **AI Engineer Internship at Xeven Solutions**.
The goal of this internship is to build a **real-world backend system** using modern Python technologies, focusing on authentication, database design, and API development.

---

## 🎯 Objective

Build a backend system that provides:

- User Registration (Sign Up)
- User Login (Authentication)
- JWT Token-based Security
- Chatbot API (Dummy AI Response)
- Store Chat History in PostgreSQL
- Retrieve User-specific Chat History

---

## 🛠️ Tech Stack

- **FastAPI** - Backend Framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Pydantic** - Data Validation
- **JWT (python-jose)** - Authentication
- **Passlib (bcrypt)** - Password Hashing
- **Uvicorn** - ASGI Server

---

## 📂 Project Structure

```
app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── auth.py
│   └── chat.py
├── services/
│   └── chatbot.py
├── utils/
│   ├── hashing.py
│   └── token.py
└── dependencies.py
```

---

## ⚙️ Features

### 🔐 Authentication System
- User Signup (`/auth/register`)
- User Login (`/auth/login`)
- Password hashing using bcrypt
- JWT token generation

---

### 💬 Chatbot API
- Endpoint: `/chat/`
- Accepts user message
- Returns dummy response:

```
Hello! How can I help you today?
```

- Stores chat history in PostgreSQL

---

### 🗂️ Chat History
- Each message is saved in database
- Linked with user using Foreign Key
- Users can retrieve their chat history

---

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login user & get JWT |
| POST | /chat/ | Send message to chatbot |
| GET | /chat/history | Get user chat history |

---

## 🗄️ Database Schema

### Users Table
- id (Primary Key)
- username
- email (Unique)
- password (Hashed)

### Conversations Table
- id
- user_message
- bot_response
- user_id (Foreign Key)

---

## 🚀 How to Run the Project

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL
Create database:

```sql
CREATE DATABASE chatbot_db;
```

### 3. Run server

```bash
uvicorn app.main:app --reload
```

### 4. Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 📚 Learning Outcomes

Through this internship, I learned:

- FastAPI backend development
- PostgreSQL database integration
- SQLAlchemy ORM relationships
- JWT authentication system
- Secure password hashing
- REST API design principles

---

## 🏢 Organization
Xeven Solutions Internship Program

## 👩‍💻 Author
**Tanzeela Fatima**
Information Technology Undergraduate
GitHub: https://github.com/Fatima-progmmer
LinkedIn: https://www.linkedin.com/in/tanzeela-fatima-47861b2b7/

## ⭐ Status
🚧 Project is currently under development as part of internship tasks.
