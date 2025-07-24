#!/bin/bash

# Production startup script
# This script sets up the environment and starts the FastAPI application

echo "Starting RAG Chatbot API..."

# Ensure database tables are created
echo "Setting up database..."

# Start the application
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WORKERS:-1}
