# 🚀 AI Engineering Internship – Xeven Solutions

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-⚡-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-🐘-336791?style=flat&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=flat&logo=jsonwebtokens&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow?style=flat)

👩‍💻 **Intern:** Tanzeela Fatima
📍 **Program:** AI Engineer Internship
🏢 **Company:** Xeven Solutions
📅 **Duration:** Internship Progress (Day 1 → Current)

## 📌 Overview

This repository contains my complete learning journey during the AI Engineer Internship at Xeven Solutions. It includes hands-on practice, backend development using FastAPI, database integration with PostgreSQL, authentication systems, and building a Chatbot API.

The goal of this internship is to learn how to build scalable backend systems using modern Python technologies.

## 🧠 What I Learned (Day-by-Day Progress)

### 📘 Day 1–3: Python & Backend Fundamentals
- Python basics revision
- Functions, loops, conditions
- Understanding backend concepts
- API basics (Request/Response cycle)

### 📘 Day 4–6: Data Structures & Problem Solving
- Arrays, strings, hashing
- LeetCode practice problems
- Logical thinking improvement
- Basic DSA challenges (Move Zeroes, 3Sum, etc.)

### 📘 Day 7–10: Introduction to FastAPI
- What is FastAPI?
- Creating first API endpoints
- Understanding path & query parameters
- Swagger UI (`/docs`) usage
- Basic routing system

### 📘 Day 11–15: Database Fundamentals (PostgreSQL)
- Introduction to databases
- Tables, rows, primary & foreign keys
- PostgreSQL setup
- Creating database: `chatbot_db`
- Connecting FastAPI with PostgreSQL using SQLAlchemy

### 📘 Day 16–20: SQLAlchemy ORM
- Creating models (`User`, `Conversation`)
- Relationships: One-to-Many (User → Conversations)
- Database session management
- CRUD operations

### 📘 Day 21–25: Authentication System
- User Registration API (`/auth/register`)
- User Login API (`/auth/login`)
- Password hashing using bcrypt (passlib)
- Input validation using Pydantic schemas
- Duplicate email handling

### 📘 Day 26–28: JWT Authentication
- JSON Web Token (JWT) concept
- Token generation using `python-jose`
- Token verification
- Protected routes using `OAuth2PasswordBearer`

### Chatbot API Development
- Built Chat API (`POST /chat`)
- Dummy chatbot response system:
  ```text
  Hello! How can I help you today?
  ```
- Stored chat conversations in PostgreSQL
- Linked messages with user ID
  
## ⚙️ Tech Stack

- Python 🐍
- FastAPI ⚡
- PostgreSQL 🐘
- SQLAlchemy
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- Uvicorn


## 🎯 Key Learning Outcomes

- Backend API development with FastAPI
- Real-world authentication systems
- JWT-based security implementation
- PostgreSQL database design
- ORM relationships (One-to-Many)
- Building production-style project structure

## 🚧 Challenges Faced

- Database connection issues
- Model mismatch errors
- 500 Internal Server Errors debugging
- JWT implementation understanding
- Dependency injection in FastAPI

## 📈 Future Improvements

- Integrate real AI chatbot (OpenAI API)
- Add frontend UI (React/Next.js)
- Add pagination for chat history
- Add logging & monitoring
- Write unit tests (pytest)

## 🙌 Acknowledgment

Special thanks to **Xeven Solutions** for providing this internship opportunity and guiding me through real-world backend development.
