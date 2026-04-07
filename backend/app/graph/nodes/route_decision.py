"""
Routing decision node.

Determines which subgraph or node to execute next based on classified intent.

WHY PYTHON ROUTING INSTEAD OF LLM:
- Faster (no API call)
- Deterministic and predictable
- Cost-effective
- Easier to debug and test
- No risk of incorrect routing
"""

import logging
from typing import Dict, Any, Literal

from backend.app.graph.state import AgentState

logger = logging.getLogger(__name__)

# Type alias for valid routes
RouteDestination = Literal[
    "search_subgraph",
    "comparison_subgraph",
    "order_subgraph",
    "general_chat",
]


def route_by_intent(state: AgentState) -> RouteDestination:
    """
    Deterministic routing function based on intent.

    This is used by LangGraph's conditional edge to determine
    the next node/subgraph to execute.

    Args:
        state: Current agent state

    Returns:
        Name of the next node or subgraph to execute
    """
    intent = state.get("intent", "chat")
    products = state.get("products", [])

    logger.info(f"=== ROUTING DECISION ===")
    logger.info(f"Intent: {intent}")
    logger.info(f"Products in state: {len(products) if products else 0}")

    # Route to appropriate subgraph based on intent
    if intent == "search":
        logger.info("→ Routing to SEARCH SUBGRAPH")
        return "search_subgraph"

    elif intent == "compare":
        # Can only compare if we have products in state
        if products and len(products) > 0:
            logger.info("→ Routing to COMPARISON SUBGRAPH")
            return "comparison_subgraph"
        else:
            logger.info("→ No products to compare, routing to GENERAL CHAT")
            return "general_chat"

    elif intent == "order":
        # Can only order if we have products to choose from
        if products and len(products) > 0:
            logger.info("→ Routing to ORDER SUBGRAPH")
            return "order_subgraph"
        else:
            logger.info("→ No products to order, routing to GENERAL CHAT")
            return "general_chat"

    elif intent == "cart":
        logger.info("→ Routing to ORDER SUBGRAPH (cart management)")
        return "order_subgraph"

    else:  # intent == "chat" or unknown
        logger.info("→ Routing to GENERAL CHAT")
        return "general_chat"
