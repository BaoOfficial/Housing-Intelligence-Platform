"""
Services - Only embedding service needed for ChromaDB seeding
"""
from .embedding_service import embedding_service, EmbeddingService

__all__ = ["embedding_service", "EmbeddingService"]
