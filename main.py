from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form, Header
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Memory, User
from memory import store_message, get_history
from groq_client import call_groq
from rag_pipeline import load_pdf, create_vectorstore, query_rag
from auth import hash_password, verify_password, create_access_token, decode_access_token
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import logging

load_dotenv()

Base.metadata.create_all(bind=engine)
app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return {"msg": "User created"}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/chat")
async def chat(
    session_id: str = Form(...),
    message: str = Form(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    store_message(db, session_id, "user", message)
    history = get_history(db, session_id)
    messages = [{"role": h.role, "content": h.content} for h in history]
    response = call_groq(messages)
    store_message(db, session_id, "assistant", response)
    return {"response": response}

@app.post("/chat_pdf")
async def chat_pdf(
    question: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    docs = load_pdf(tmp_path)
    vectorstore = create_vectorstore(docs)
    response = query_rag(question, vectorstore)
    return {"response": response}

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "RAG Chatbot API is running"}

@app.get("/health")
async def detailed_health():
    return {
        "status": "healthy",
        "service": "RAG Chatbot API",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'unknown')}")
    logger.info(f"Port: {os.getenv('PORT', 'unknown')}")
    logger.info("Startup complete")

if __name__ == "__main__":
    port = 8080
    uvicorn.run(app, host="0.0.0.0", port=port)
