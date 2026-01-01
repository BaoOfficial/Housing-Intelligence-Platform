"""
Text embedding service using OpenAI
"""
from openai import OpenAI
from typing import List
from ..config import settings


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_EMBEDDING_MODEL

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch)

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        # OpenAI supports batch embedding
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]


# Global instance
embedding_service = EmbeddingService()
