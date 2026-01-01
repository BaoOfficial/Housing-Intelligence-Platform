"""
Chat API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from ..database import get_db
from ..schemas.chat import ChatMessageRequest, ChatMessageResponse
from ..services.ai_engine_client import ai_engine_client
from ..services.property_service import PropertyService

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Process a chat message and return AI response

    Flow:
    1. Send message to AI-Engine (agent decides what tools to use)
    2. AI agent uses search_properties tool if needed
    3. Extract search params used by the agent
    4. Query properties based on agent's search params
    5. Return AI response with property data for frontend display
    """
    try:
        # Call AI-Engine - the agent will use search_properties tool intelligently
        ai_response = await ai_engine_client.chat(
            message=request.message,
            context={},  # No pre-querying - let agent decide
            conversation_id=request.conversation_id
        )

        # Extract search parameters used by the agent's search_properties tool
        search_params = ai_response.get("search_params", {})

        # Query properties if the agent searched for them
        property_context = []
        if search_params:
            property_context = PropertyService.get_properties_context_for_ai(
                db=db,
                area=search_params.get("area"),
                property_type=search_params.get("property_type"),
                bedrooms=search_params.get("bedrooms"),
                min_rent=search_params.get("min_rent"),
                max_rent=search_params.get("max_rent"),
                limit=search_params.get("limit", 10)
            )

        # Generate conversation ID if not provided
        conversation_id = ai_response.get("conversation_id") or request.conversation_id or str(uuid.uuid4())

        return ChatMessageResponse(
            response=ai_response.get("response", ""),
            conversation_id=conversation_id,
            sources=ai_response.get("sources", []),
            properties=property_context  # Properties found by agent's tool
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.get("/health")
async def chat_health():
    """Check chat endpoint and AI-Engine connectivity"""
    try:
        ai_health = await ai_engine_client.health_check()
        return {
            "status": "healthy",
            "ai_engine": ai_health
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }
