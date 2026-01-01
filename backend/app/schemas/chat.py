"""
Pydantic schemas for Chat-related requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class ChatMessageRequest(BaseModel):
    """Schema for chat message request"""
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    """Schema for chat message response"""
    response: str
    conversation_id: str
    sources: Optional[List[Dict[str, Any]]] = []
    properties: Optional[List[Dict[str, Any]]] = []
