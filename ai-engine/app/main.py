"""
Main FastAPI application for AI Engine
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI/RAG service for Housing Intelligence Platform"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Housing Intelligence Platform - AI Engine",
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    from .core.vector_db import vector_db

    try:
        collection_count = vector_db.get_collection_count()
    except:
        collection_count = "unavailable"

    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "openai_model": settings.OPENAI_MODEL,
        "embedding_model": settings.OPENAI_EMBEDDING_MODEL,
        "chromadb_documents": collection_count
    }


# Import and include routers
from .api import chat

app.include_router(chat.router, prefix="/ai/v1", tags=["Chat"])
