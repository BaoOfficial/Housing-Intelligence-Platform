"""
Chat API endpoints - Simplified with LangGraph ReAct agent
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict
from ..core.agent import housing_agent
import json

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    context: Optional[Dict] = None  # Deprecated - agent uses tools instead
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    conversation_id: str
    sources: Optional[list] = []
    search_params: Optional[Dict] = {}  # Parameters used by search_properties tool


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint using LangGraph ReAct agent

    The agent automatically:
    - Reasons about what information is needed
    - Uses tools to search reviews and get statistics
    - Combines property context with review data
    - Generates helpful responses
    """
    try:
        # Use conversation_id as thread_id for memory
        thread_id = request.conversation_id or "default"

        # Invoke the ReAct agent
        result = await housing_agent.ainvoke(
            user_message=request.message,
            context=request.context,
            thread_id=thread_id
        )

        # Extract sources from agent's tool calls
        # The agent messages contain tool call information
        sources = []
        messages = result.get("messages", [])

        # Look for tool calls in messages to extract sources
        for msg in messages:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    if tool_call.get('name') == 'search_tenant_reviews':
                        # This was a review search - could extract as source
                        sources.append({
                            "tool": "search_tenant_reviews",
                            "args": tool_call.get('args', {})
                        })

        return ChatResponse(
            response=result["response"],
            conversation_id=thread_id,
            sources=sources[:5],  # Limit to 5 sources
            search_params=result.get("search_params", {})  # Include search params for backend
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat with agent: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint

    Returns a streaming response where the agent's response
    is sent in chunks as it's generated.
    """
    try:
        thread_id = request.conversation_id or "default"

        async def generate():
            """Generate response chunks"""
            async for message in housing_agent.astream(
                user_message=request.message,
                context=request.context,
                thread_id=thread_id
            ):
                # Convert message to dict and send as JSON
                if hasattr(message, 'content'):
                    chunk = {"content": message.content, "type": str(type(message).__name__)}
                    yield f"data: {json.dumps(chunk)}\n\n"

            # Send done signal
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error streaming chat: {str(e)}"
        )
