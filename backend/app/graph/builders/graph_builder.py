"""
Main graph builder.

This module constructs the complete LangGraph agent by:
1. Creating the main graph structure
2. Adding all nodes
3. Integrating subgraphs
4. Setting up routing logic
5. Configuring checkpointer for state persistence

ARCHITECTURE:
    User Input
        ↓
    [classify_intent] ← Gemini classifies user intent
        ↓
    [route_by_intent] ← Python routing (not LLM!)
        ├→ search_subgraph
        ├→ comparison_subgraph
        ├→ order_subgraph
        └→ general_chat
        ↓
    [format_response] ← Ensure response is ready
        ↓
    Output to User

CHECKPOINTER:
The checkpointer saves state after each node execution.
This enables conversation continuity and multi-turn interactions.
"""

import logging
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from backend.app.graph.state import AgentState
from backend.app.graph.nodes import (
    classify_intent_node,
    route_by_intent,
    general_chat_node,
    format_response_node,
)
from backend.app.graph.subgraphs import (
    build_search_subgraph,
    build_comparison_subgraph,
    build_order_subgraph,
)

logger = logging.getLogger(__name__)


def build_agent_graph():
    """
    Build and compile the complete agent graph.

    This is the main function that constructs the entire LangGraph agent.

    Returns:
        Compiled StateGraph with checkpointer
    """
    logger.info("========================================")
    logger.info("Building ShopGraph AI Agent")
    logger.info("========================================")

    # Create the main graph
    graph = StateGraph(AgentState)

    # ========================================
    # Add Main Nodes
    # ========================================

    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("general_chat", general_chat_node)
    graph.add_node("format_response", format_response_node)

    logger.info("✓ Added main nodes")

    # ========================================
    # Add Subgraphs
    # ========================================
    # Subgraphs are integrated as nodes in the main graph.
    # Each subgraph is a complete workflow that returns to the main graph.

    search_subgraph = build_search_subgraph()
    comparison_subgraph = build_comparison_subgraph()
    order_subgraph = build_order_subgraph()

    graph.add_node("search_subgraph", search_subgraph)
    graph.add_node("comparison_subgraph", comparison_subgraph)
    graph.add_node("order_subgraph", order_subgraph)

    logger.info("✓ Added subgraphs")

    # ========================================
    # Define Main Flow
    # ========================================

    # Entry point
    graph.set_entry_point("classify_intent")

    # After intent classification, route to appropriate subgraph
    # This is CONDITIONAL ROUTING using Python function
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,  # Router function returns destination name
        {
            "search_subgraph": "search_subgraph",
            "comparison_subgraph": "comparison_subgraph",
            "order_subgraph": "order_subgraph",
            "general_chat": "general_chat",
        }
    )

    logger.info("✓ Added conditional routing")

    # After each subgraph completes, go to format_response
    graph.add_edge("search_subgraph", "format_response")
    graph.add_edge("comparison_subgraph", "format_response")
    graph.add_edge("order_subgraph", "format_response")
    graph.add_edge("general_chat", "format_response")

    # After formatting, end
    graph.add_edge("format_response", END)

    logger.info("✓ Added edges to END")

    # ========================================
    # Configure Checkpointer
    # ========================================
    # The checkpointer persists graph state between invocations.
    #
    # WHY CHECKPOINTER:
    # 1. Conversation continuity - resume conversations
    # 2. Multi-turn interactions - remember search results
    # 3. Workflow state - track progress in multi-step flows
    #
    # WHAT GETS CHECKPOINTED:
    # - Complete AgentState after each node
    # - Conversation messages
    # - Search results (products)
    # - Selected products
    # - Cart and order state
    #
    # FOR DEVELOPMENT:
    # Using MemorySaver (in-memory checkpointer)
    #
    # FOR PRODUCTION:
    # Replace with persistent checkpointer:
    # - MongoDBCheckpointer
    # - RedisSaver
    # - PostgresSaver

    checkpointer = MemorySaver()

    logger.info("✓ Configured checkpointer (MemorySaver)")

    # ========================================
    # Compile Graph
    # ========================================

    compiled_graph = graph.compile(checkpointer=checkpointer)

    logger.info("✓ Graph compiled successfully")
    logger.info("========================================")
    logger.info("Agent ready for execution")
    logger.info("========================================")

    return compiled_graph


# Singleton instance
_agent_graph = None


def get_agent_graph():
    """
    Get or create the agent graph singleton.

    Returns:
        Compiled agent graph
    """
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = build_agent_graph()
    return _agent_graph
