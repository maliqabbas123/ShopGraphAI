"""
Search Subgraph.

Multi-step workflow for product search:
1. Extract filters from user input (LLM)
2. Call search tool
3. Format results
4. Update state with products

WHY A SUBGRAPH:
- Encapsulates complex multi-step logic
- Reusable across different entry points
- Separates concerns from main graph
- Makes testing easier
"""

import logging
from typing import Dict, Any
from langchain_core.messages import AIMessage

from backend.app.graph.state import AgentState
from backend.app.graph.tools import search_products_tool
from backend.app.services.gemini_service import get_gemini_service

logger = logging.getLogger(__name__)


async def extract_filters_node(state: AgentState) -> Dict[str, Any]:
    """
    Extract search filters from user input using Gemini.

    This node uses LLM to parse natural language into structured filters.

    Args:
        state: Current agent state

    Returns:
        State update with extracted filters
    """
    logger.info("=== EXTRACT FILTERS NODE ===")

    user_input = state.get("user_input", "")

    gemini_service = get_gemini_service()
    filters = await gemini_service.extract_search_filters(user_input)

    logger.info(f"Extracted filters: {filters}")

    return {"filters": filters}


async def execute_search_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute product search using extracted filters.

    Calls the search tool with filters from state.

    Args:
        state: Current agent state

    Returns:
        State update with search results
    """
    logger.info("=== EXECUTE SEARCH NODE ===")

    filters = state.get("filters", {})

    # Call search tool
    result = await search_products_tool.ainvoke(filters)

    if result.get("success"):
        products = result.get("products", [])
        logger.info(f"Search successful: {len(products)} products found")

        return {
            "products": products,
        }
    else:
        error = result.get("error", "Unknown search error")
        logger.error(f"Search failed: {error}")

        return {
            "products": [],
            "errors": [error]
        }


async def format_search_response_node(state: AgentState) -> Dict[str, Any]:
    """
    Format search results into user-friendly response.

    Args:
        state: Current agent state

    Returns:
        State update with formatted response
    """
    logger.info("=== FORMAT SEARCH RESPONSE NODE ===")

    products = state.get("products", [])
    filters = state.get("filters", {})

    if not products or len(products) == 0:
        response = "I couldn't find any products matching your criteria. Try adjusting your search."
        logger.info("No products found")
    else:
        # Build response message
        count = len(products)
        filter_desc = ", ".join([f"{k}={v}" for k, v in filters.items()]) if filters else "your search"

        response = f"I found {count} product{'s' if count != 1 else ''} matching {filter_desc}. "

        if count <= 5:
            response += "Here's what I found:"
        else:
            response += f"Here are the top {min(5, count)} results:"

        # Add product summary (limit to 5)
        for i, product in enumerate(products[:5]):
            response += f"\n{i+1}. {product['title']} by {product['brand']} - ${product['price']}"

        if count > 5:
            response += f"\n\n...and {count - 5} more options. You can ask me to compare specific products or refine your search."

        logger.info(f"Formatted response for {count} products")

    return {
        "final_response": response,
        "messages": [AIMessage(content=response)]
    }


# Build the search subgraph
def build_search_subgraph():
    """
    Build and return the search subgraph.

    Flow:
        extract_filters → execute_search → format_response

    Returns:
        Compiled StateGraph for search workflow
    """
    from langgraph.graph import StateGraph, END

    logger.info("Building search subgraph")

    # Create subgraph
    subgraph = StateGraph(AgentState)

    # Add nodes
    subgraph.add_node("extract_filters", extract_filters_node)
    subgraph.add_node("execute_search", execute_search_node)
    subgraph.add_node("format_response", format_search_response_node)

    # Define edges
    subgraph.add_edge("extract_filters", "execute_search")
    subgraph.add_edge("execute_search", "format_response")
    subgraph.add_edge("format_response", END)

    # Set entry point
    subgraph.set_entry_point("extract_filters")

    return subgraph.compile()
