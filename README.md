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

The API will be available at `http://localhost:8000`

## Railway Deployment

### Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

### Manual Deployment

1. **Create a Railway account** at [railway.app](https://railway.app)

2. **Create a new project** and connect your GitHub repository

3. **Add a PostgreSQL database**:
   - Go to your Railway dashboard
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically create a database and provide connection details

4. **Configure environment variables** in Railway dashboard:
   ```env
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   GROQ_API_KEY=your_groq_api_key_here
   JWT_SECRET_KEY=your_very_secure_secret_key_here
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   ENVIRONMENT=production
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

5. **Deploy**: Railway will automatically build and deploy your application

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GROQ_API_KEY` | Your Groq API key | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes |
| `JWT_ALGORITHM` | JWT algorithm (default: HS256) | No |
| `JWT_EXPIRATION_HOURS` | Token expiration in hours (default: 24) | No |
| `ENVIRONMENT` | Environment name (production/development) | No |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | No |

## API Endpoints

### Authentication

- `POST /signup` - Create a new user account
- `POST /login` - Login and get access token

### Chat

- `POST /chat` - Send a message and get AI response
- `POST /chat_pdf` - Upload PDF and ask questions about it

### Health

- `GET /` - Basic health check
- `GET /health` - Detailed health information
- `GET /docs` - Interactive API documentation

## API Usage Examples

### Sign Up
```bash
curl -X POST "https://your-app.railway.app/signup" \
  -F "email=user@example.com" \
  -F "password=securepassword"
```

### Login
```bash
curl -X POST "https://your-app.railway.app/login" \
  -F "email=user@example.com" \
  -F "password=securepassword"
```

### Chat
```bash
curl -X POST "https://your-app.railway.app/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "session_id=session123" \
  -F "message=Hello, how are you?"
```

### PDF Chat
```bash
curl -X POST "https://your-app.railway.app/chat_pdf" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "question=What is this document about?" \
  -F "file=@document.pdf"
```

## Alternative Free Hosting Options

If Railway doesn't work for you, here are other free options:

### 1. Render
- Free tier with 512MB RAM
- Automatic deploys from Git
- Built-in PostgreSQL

### 2. Fly.io
- Free allowance: 3 VMs with 256MB RAM
- Global deployment
- Dockerfile support

### 3. Heroku (Limited Free)
- Popular platform
- Easy deployment
- Add-on ecosystem

### 4. DigitalOcean App Platform
- Free starter tier
- Container support
- Database add-ons

## Production Considerations

- Use strong JWT secret keys
- Configure CORS properly for your frontend
- Set up monitoring and logging
- Consider rate limiting
- Use environment-specific configurations
- Regular database backups
- SSL/TLS certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
