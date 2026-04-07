"""
Intent classification node.

Determines what the user wants to do based on their message.
This is a critical routing decision point in the graph.
"""

import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage

from backend.app.graph.state import AgentState
from backend.app.services.gemini_service import get_gemini_service

logger = logging.getLogger(__name__)


async def classify_intent_node(state: AgentState) -> Dict[str, Any]:
    """
    Classify user intent using Gemini LLM.

    This node analyzes the user's input and determines their intent.
    The intent drives routing decisions downstream.

    WHY USE LLM HERE:
    - Natural language understanding required
    - Context-dependent classification
    - Handles variations in phrasing

    Args:
        state: Current agent state

    Returns:
        State update with classified intent
    """
    logger.info("=== CLASSIFY INTENT NODE ===")

    user_input = state.get("user_input", "")
    if not user_input:
        logger.warning("No user input found in state")
        return {"intent": "chat"}

    # Get conversation history for context
    messages = state.get("messages", [])
    conversation_history = [
        msg.content for msg in messages[-6:]  # Last 3 exchanges
        if hasattr(msg, 'content')
    ]

    # Call Gemini to classify intent
    gemini_service = get_gemini_service()
    intent = await gemini_service.classify_intent(user_input, conversation_history)

    logger.info(f"User input: '{user_input}'")
    logger.info(f"Classified intent: {intent}")

    # Add user message to messages
    updates = {
        "intent": intent,
        "messages": [HumanMessage(content=user_input)]
    }

    return updates
