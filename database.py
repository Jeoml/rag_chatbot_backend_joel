from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

try:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not found in environment variables")
    
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    # Test connection
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    logger.info("Database connection successful")
except SQLAlchemyError as e:
    logger.error(f"Database connection failed: {e}")
    raise

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
