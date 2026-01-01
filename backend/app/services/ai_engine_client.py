"""
AI-Engine client for communicating with the AI/RAG service
"""
import httpx
from typing import Dict, List, Any, Optional
from ..config import settings


class AIEngineClient:
    """Client for AI-Engine service"""

    def __init__(self):
        self.base_url = settings.AI_ENGINE_URL
        self.timeout = 30.0  # 30 seconds timeout for LLM calls

    async def chat(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a chat message to AI-Engine

        Args:
            message: User message
            context: Additional context (property data, etc.)
            conversation_id: Optional conversation ID

        Returns:
            AI response with sources and conversation_id
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "message": message,
                "context": context or {},
                "conversation_id": conversation_id
            }

            response = await client.post(
                f"{self.base_url}/ai/v1/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def search_reviews(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant reviews in ChromaDB

        Args:
            query: Search query
            filters: Metadata filters (area, property_type, etc.)
            limit: Maximum number of results

        Returns:
            List of relevant reviews
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "query": query,
                "filters": filters or {},
                "limit": limit
            }

            response = await client.post(
                f"{self.base_url}/ai/v1/search/reviews",
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def analyze_intent(
        self,
        message: str
    ) -> Dict[str, Any]:
        """
        Analyze user message intent

        Args:
            message: User message

        Returns:
            Intent classification and extracted entities
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {"message": message}

            response = await client.post(
                f"{self.base_url}/ai/v1/analyze/intent",
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def health_check(self) -> Dict[str, Any]:
        """
        Check AI-Engine health status

        Returns:
            Health status information
        """
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()


# Singleton instance
ai_engine_client = AIEngineClient()
