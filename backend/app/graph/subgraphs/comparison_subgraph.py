"""
Comparison Subgraph.

Multi-step workflow for product comparison:
1. Resolve which products to compare
2. Call comparison tool
3. Generate LLM explanation
4. Format response

WHY A SUBGRAPH:
- Comparison is a multi-step process
- Needs to handle various input formats ("first two", "all", specific indices)
- Can be called from different contexts
- Isolates comparison logic
"""

import logging
from typing import Dict, Any, List
from langchain_core.messages import AIMessage
import re

from backend.app.graph.state import AgentState
from backend.app.graph.tools import compare_products_tool
from backend.app.services.gemini_service import get_gemini_service

logger = logging.getLogger(__name__)


async def resolve_products_node(state: AgentState) -> Dict[str, Any]:
    """
    Resolve which products user wants to compare.

    Handles various formats:
    - "compare the first two"
    - "compare all"
    - "compare product 1 and 3"

    Args:
        state: Current agent state

    Returns:
        State update with selected product IDs
    """
    logger.info("=== RESOLVE PRODUCTS NODE ===")

    user_input = state.get("user_input", "").lower()
    products = state.get("products", [])

    if not products or len(products) == 0:
        logger.warning("No products available to compare")
        return {
            "selected_product_ids": [],
            "errors": ["No products available to compare. Please search first."]
        }

    # Parse user intent for which products to compare
    selected_ids = []

    # Check for "all"
    if "all" in user_input:
        selected_ids = [p["_id"] for p in products[:5]]  # Limit to 5
        logger.info(f"Comparing all products: {len(selected_ids)}")

    # Check for "first X" or "top X"
    elif match := re.search(r"(?:first|top)\s+(\d+)", user_input):
        count = int(match.group(1))
        selected_ids = [p["_id"] for p in products[:count]]
        logger.info(f"Comparing first {count} products")

    # Check for specific indices like "1 and 3" or "1, 2, 3"
    elif match := re.findall(r"\b(\d+)\b", user_input):
        indices = [int(i) - 1 for i in match if int(i) <= len(products)]  # Convert to 0-indexed
        selected_ids = [products[i]["_id"] for i in indices if i < len(products)]
        logger.info(f"Comparing products at indices: {[i+1 for i in indices]}")

    # Default: compare first 3
    else:
        count = min(3, len(products))
        selected_ids = [p["_id"] for p in products[:count]]
        logger.info(f"Defaulting to first {count} products")

    if len(selected_ids) < 2:
        logger.warning("Need at least 2 products for comparison")
        return {
            "selected_product_ids": [],
            "errors": ["Need at least 2 products to compare. Please specify which products."]
        }

    return {"selected_product_ids": selected_ids}


async def execute_comparison_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute product comparison using comparison tool.

    Args:
        state: Current agent state

    Returns:
        State update with comparison results
    """
    logger.info("=== EXECUTE COMPARISON NODE ===")

    selected_ids = state.get("selected_product_ids", [])

    if len(selected_ids) < 2:
        logger.error("Insufficient products for comparison")
        return {
            "comparison_result": None,
            "errors": ["Need at least 2 products to compare"]
        }

    # Call comparison tool
    result = await compare_products_tool.ainvoke({"product_ids": selected_ids})

    if result.get("success"):
        comparison = result.get("comparison", {})
        logger.info("Comparison generated successfully")

        return {"comparison_result": comparison}
    else:
        error = result.get("error", "Comparison failed")
        logger.error(f"Comparison error: {error}")

        return {
            "comparison_result": None,
            "errors": [error]
        }


async def generate_comparison_explanation_node(state: AgentState) -> Dict[str, Any]:
    """
    Generate natural language explanation of comparison using Gemini.

    Args:
        state: Current agent state

    Returns:
        State update with formatted response
    """
    logger.info("=== GENERATE COMPARISON EXPLANATION NODE ===")

    comparison_result = state.get("comparison_result")

    if not comparison_result:
        response = "I couldn't generate the comparison. Please try again."
        logger.warning("No comparison result to explain")
    else:
        # Get products from comparison
        products = comparison_result.get("products", [])

        # Generate explanation using Gemini
        gemini_service = get_gemini_service()
        explanation = await gemini_service.generate_comparison_explanation(
            products=products,
            comparison_data=comparison_result
        )

        # Build full response with structured data + explanation
        response = "Here's the comparison:\n\n"

        # Add price comparison
        for i, prod in enumerate(products):
            response += f"{i+1}. {prod['title']} - ${prod['price']} (Rating: {prod['rating']}/5)\n"

        response += f"\n{explanation}"

        logger.info("Comparison explanation generated")

    return {
        "final_response": response,
        "messages": [AIMessage(content=response)]
    }


# Build the comparison subgraph
def build_comparison_subgraph():
    """
    Build and return the comparison subgraph.

    Flow:
        resolve_products → execute_comparison → generate_explanation

    Returns:
        Compiled StateGraph for comparison workflow
    """
    from langgraph.graph import StateGraph, END

    logger.info("Building comparison subgraph")

    # Create subgraph
    subgraph = StateGraph(AgentState)

    # Add nodes
    subgraph.add_node("resolve_products", resolve_products_node)
    subgraph.add_node("execute_comparison", execute_comparison_node)
    subgraph.add_node("generate_explanation", generate_comparison_explanation_node)

    # Define edges
    subgraph.add_edge("resolve_products", "execute_comparison")
    subgraph.add_edge("execute_comparison", "generate_explanation")
    subgraph.add_edge("generate_explanation", END)

    # Set entry point
    subgraph.set_entry_point("resolve_products")

    return subgraph.compile()
