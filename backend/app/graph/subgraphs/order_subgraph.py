"""
Order Subgraph.

Multi-step workflow for order placement:
1. Resolve which product to order
2. Check stock
3. Place order
4. Format confirmation

WHY A SUBGRAPH:
- Order flow has multiple steps that must succeed
- Needs validation at each step
- Clear failure points
- Transactional-style workflow
"""

import logging
from typing import Dict, Any
from langchain_core.messages import AIMessage
import re

from backend.app.graph.state import AgentState
from backend.app.graph.tools import check_stock_tool, place_order_tool

logger = logging.getLogger(__name__)


async def resolve_product_node(state: AgentState) -> Dict[str, Any]:
    """
    Resolve which product user wants to order.

    Handles formats like:
    - "order the first one"
    - "buy product 2"
    - "order the cheapest"

    Args:
        state: Current agent state

    Returns:
        State update with selected product
    """
    logger.info("=== RESOLVE PRODUCT NODE ===")

    user_input = state.get("user_input", "").lower()
    products = state.get("products", [])

    if not products or len(products) == 0:
        logger.warning("No products available to order")
        return {
            "selected_product": None,
            "errors": ["No products available. Please search first."]
        }

    selected_product = None

    # Check for specific index
    if match := re.search(r"(?:first|product|number)\s*(\d+|one|two|three)", user_input):
        index_str = match.group(1)
        if index_str in ["one", "first"]:
            index = 0
        elif index_str == "two":
            index = 1
        elif index_str == "three":
            index = 2
        else:
            index = int(index_str) - 1  # Convert to 0-indexed

        if index < len(products):
            selected_product = products[index]
            logger.info(f"Selected product at index {index+1}")

    # Check for "cheapest" or "lowest price"
    elif "cheapest" in user_input or "lowest price" in user_input:
        selected_product = min(products, key=lambda p: p["price"])
        logger.info("Selected cheapest product")

    # Check for "best" or "highest rated"
    elif "best" in user_input or "highest rated" in user_input or "top rated" in user_input:
        selected_product = max(products, key=lambda p: p["rating"])
        logger.info("Selected highest rated product")

    # Default: first product
    else:
        selected_product = products[0]
        logger.info("Defaulting to first product")

    if not selected_product:
        logger.error("Could not resolve product")
        return {
            "selected_product": None,
            "errors": ["Could not identify which product to order."]
        }

    return {"selected_product": selected_product}


async def check_stock_node(state: AgentState) -> Dict[str, Any]:
    """
    Verify product is in stock before ordering.

    Args:
        state: Current agent state

    Returns:
        State update with stock status
    """
    logger.info("=== CHECK STOCK NODE ===")

    selected_product = state.get("selected_product")

    if not selected_product:
        logger.error("No product selected")
        return {"errors": ["No product selected for stock check"]}

    product_id = selected_product["_id"]

    # Call stock check tool
    result = await check_stock_tool.ainvoke({"product_id": product_id})

    if result.get("success"):
        if result.get("in_stock"):
            logger.info(f"Product {product_id} is in stock")
            return {}  # Continue to order
        else:
            logger.warning(f"Product {product_id} is out of stock")
            return {
                "errors": [f"Sorry, {selected_product['title']} is currently out of stock."]
            }
    else:
        error = result.get("error", "Stock check failed")
        logger.error(f"Stock check error: {error}")
        return {"errors": [error]}


async def place_order_node(state: AgentState) -> Dict[str, Any]:
    """
    Place the order for selected product.

    Args:
        state: Current agent state

    Returns:
        State update with order confirmation
    """
    logger.info("=== PLACE ORDER NODE ===")

    selected_product = state.get("selected_product")
    errors = state.get("errors", [])

    # Don't place order if there are errors from previous steps
    if errors:
        logger.warning("Skipping order placement due to previous errors")
        return {}

    if not selected_product:
        logger.error("No product selected")
        return {"errors": ["No product to order"]}

    product_id = selected_product["_id"]

    # Call order placement tool
    result = await place_order_tool.ainvoke({"product_id": product_id})

    if result.get("success"):
        order_data = {
            "order_id": result.get("order_id"),
            "product_title": result.get("product_title"),
            "total_amount": result.get("total_amount"),
            "currency": result.get("currency", "USD"),
            "status": result.get("status", "confirmed")
        }

        logger.info(f"Order placed successfully: {order_data['order_id']}")

        return {"order_state": order_data}
    else:
        error = result.get("error", "Order placement failed")
        logger.error(f"Order error: {error}")
        return {"errors": [error]}


async def format_order_response_node(state: AgentState) -> Dict[str, Any]:
    """
    Format order confirmation or error message.

    Args:
        state: Current agent state

    Returns:
        State update with formatted response
    """
    logger.info("=== FORMAT ORDER RESPONSE NODE ===")

    errors = state.get("errors", [])
    order_state = state.get("order_state")

    if errors:
        response = "I couldn't complete your order:\n" + "\n".join(f"• {err}" for err in errors)
        logger.info("Formatting error response")
    elif order_state:
        response = f"""🎉 Order placed successfully!

Order ID: {order_state['order_id']}
Product: {order_state['product_title']}
Total: ${order_state['total_amount']:.2f} {order_state['currency']}
Status: {order_state['status'].title()}

Your order will be processed shortly. Thank you for shopping with us!"""
        logger.info("Formatting success response")
    else:
        response = "Something went wrong with your order. Please try again."
        logger.warning("No order state or errors found")

    return {
        "final_response": response,
        "messages": [AIMessage(content=response)]
    }


# Build the order subgraph
def build_order_subgraph():
    """
    Build and return the order subgraph.

    Flow:
        resolve_product → check_stock → place_order → format_response

    Returns:
        Compiled StateGraph for order workflow
    """
    from langgraph.graph import StateGraph, END

    logger.info("Building order subgraph")

    # Create subgraph
    subgraph = StateGraph(AgentState)

    # Add nodes
    subgraph.add_node("resolve_product", resolve_product_node)
    subgraph.add_node("check_stock", check_stock_node)
    subgraph.add_node("place_order", place_order_node)
    subgraph.add_node("format_response", format_order_response_node)

    # Define edges (sequential flow)
    subgraph.add_edge("resolve_product", "check_stock")
    subgraph.add_edge("check_stock", "place_order")
    subgraph.add_edge("place_order", "format_response")
    subgraph.add_edge("format_response", END)

    # Set entry point
    subgraph.set_entry_point("resolve_product")

    return subgraph.compile()
