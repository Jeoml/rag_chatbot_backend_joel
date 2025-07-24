# RAG Chatbot Backend API

A FastAPI-based backend for a RAG (Retrieval-Augmented Generation) chatbot with PDF processing capabilities.

## Features

- 🔐 User authentication with JWT tokens
- 💬 Chat functionality with conversation history
- 📄 PDF upload and querying capabilities
- 🔍 Vector search using FAISS
- 🤖 Integration with Groq LLM API
- 🗄️ PostgreSQL database support

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Database
- **LangChain** - LLM framework
- **FAISS** - Vector similarity search
- **Groq** - LLM API
- **BCrypt** - Password hashing

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Groq API key

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your values:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   GROQ_API_KEY=your_groq_api_key
   JWT_SECRET_KEY=your_secure_secret_key
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `https://ragchatbotbackendjoel-production.up.railway.app/docs`
