"""
Chat API endpoints.

Handles chat message processing and history retrieval.
"""

import logging
from fastapi import APIRouter, HTTPException

from backend.app.schemas import ChatMessageRequest, ChatMessageResponse, ChatHistoryResponse
from backend.app.services import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(request: ChatMessageRequest):
    """
    Send a chat message and get agent response.

    This endpoint:
    1. Receives user message
    2. Executes LangGraph agent
    3. Returns response with any products/comparisons/orders

    Args:
        request: Chat message request

    Returns:
        Agent response with optional products data
    """
    try:
        logger.info(f"Received chat message: '{request.message}' for thread: {request.thread_id}")

        # Initialize chat service
        chat_service = ChatService()

        # Process message through agent graph
        response_data = await chat_service.process_message(
            message=request.message,
            thread_id=request.thread_id
        )

        logger.info(f"Returning response for thread: {response_data['thread_id']}")

        return ChatMessageResponse(**response_data)

    except Exception as e:
        logger.error(f"Error in send_message endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{thread_id}", response_model=ChatHistoryResponse)
async def get_history(thread_id: str):
    """
    Get conversation history for a thread.

    Args:
        thread_id: Thread identifier

    Returns:
        Conversation history
    """
    try:
        logger.info(f"Fetching history for thread: {thread_id}")

        chat_service = ChatService()
        history_data = await chat_service.get_session_history(thread_id)

        if "error" in history_data:
            raise HTTPException(status_code=404, detail=history_data["error"])

        return ChatHistoryResponse(**history_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_history endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Status message
    """
    return {"status": "healthy", "service": "chat"}
