"""
General chat node.

Handles conversational responses that don't require specific actions.
"""

import logging
from typing import Dict, Any
from langchain_core.messages import AIMessage

from backend.app.graph.state import AgentState
from backend.app.services.gemini_service import get_gemini_service

logger = logging.getLogger(__name__)


async def general_chat_node(state: AgentState) -> Dict[str, Any]:
    """
    Generate general conversational response.

    This node handles:
    - Greetings
    - General questions
    - Requests that can't be fulfilled (e.g., "compare" with no products)

    Args:
        state: Current agent state

    Returns:
        State update with generated response
    """
    logger.info("=== GENERAL CHAT NODE ===")

    user_input = state.get("user_input", "")
    intent = state.get("intent", "chat")
    products = state.get("products", [])

    # Build context for response
    context = None

    # Provide helpful context if user tried an action without prerequisites
    if intent == "compare" and (not products or len(products) == 0):
        context = "User tried to compare products but no search results are available. Suggest searching for products first."
    elif intent == "order" and (not products or len(products) == 0):
        context = "User tried to order but no products are available. Suggest searching for products first."

    # Generate response using Gemini
    gemini_service = get_gemini_service()
    response_text = await gemini_service.generate_chat_response(user_input, context)

    logger.info(f"Generated response: {response_text[:100]}...")

    return {
        "final_response": response_text,
        "messages": [AIMessage(content=response_text)],
    }
