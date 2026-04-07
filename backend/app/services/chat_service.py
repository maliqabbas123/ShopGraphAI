"""
Chat service.

Business logic for chat operations.
Orchestrates graph execution and session management.
"""

import logging
from typing import Dict, Any
import uuid

from backend.app.repositories import ChatSessionRepository
from backend.app.db import get_db
from backend.app.graph import get_agent_graph, create_initial_state

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service for chat operations.

    Coordinates graph execution and session persistence.
    """

    def __init__(self):
        """Initialize chat service."""
        self.agent_graph = get_agent_graph()

    async def process_message(self, message: str, thread_id: str = None) -> Dict[str, Any]:
        """
        Process user message through the agent graph.

        This is the main entry point for chat interactions.

        Args:
            message: User's message
            thread_id: Optional thread ID (creates new if None)

        Returns:
            Dict with response data including:
                - thread_id
                - response text
                - products (if any)
                - comparison (if any)
                - order_confirmation (if any)
        """
        # Generate thread ID if not provided
        if not thread_id:
            thread_id = f"thread_{uuid.uuid4().hex[:12]}"
            logger.info(f"Created new thread: {thread_id}")

        logger.info("=" * 60)
        logger.info(f"Processing message for thread: {thread_id}")
        logger.info(f"User message: {message}")
        logger.info("=" * 60)

        # Create initial state
        initial_state = create_initial_state(user_input=message, thread_id=thread_id)

        # Execute graph with checkpointer
        # The thread_id serves as the checkpoint key
        config = {"configurable": {"thread_id": thread_id}}

        try:
            # Invoke graph (async execution through all nodes)
            final_state = await self.agent_graph.ainvoke(initial_state, config=config)

            logger.info("Graph execution completed")
            logger.info(f"Final intent: {final_state.get('intent')}")
            products = final_state.get('products') or []
            logger.info(f"Products in state: {len(products)}")

            # Extract response data
            response_data = self._extract_response_data(final_state, thread_id)

            # Save to database
            await self._save_to_database(thread_id, message, response_data)

            logger.info("=" * 60)
            logger.info("Message processing complete")
            logger.info("=" * 60)

            return response_data

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return {
                "thread_id": thread_id,
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "products": None,
                "comparison": None,
                "order_confirmation": None,
                "error": str(e)
            }

    def _extract_response_data(self, state: Dict[str, Any], thread_id: str) -> Dict[str, Any]:
        """
        Extract response data from final state.

        Args:
            state: Final graph state
            thread_id: Thread identifier

        Returns:
            Response data dict
        """
        response_text = state.get("final_response", "How can I help you?")
        products = state.get("products", [])
        comparison = state.get("comparison_result")
        order_state = state.get("order_state")
        intent = state.get("intent")

        # Convert products to API response format
        products_response = None
        if products and len(products) > 0:
            products_response = [
                {
                    "id": p["_id"],
                    "title": p["title"],
                    "brand": p["brand"],
                    "price": p["price"],
                    "rating": p["rating"],
                    "stock": p["stock"],
                    "category": p["category"],
                    "attributes": p.get("attributes", {})
                }
                for p in products[:10]  # Limit to 10 for API response
            ]

        return {
            "thread_id": thread_id,
            "response": response_text,
            "products": products_response,
            "comparison": comparison,
            "order_confirmation": order_state,
            "intent": intent
        }

    async def _save_to_database(self, thread_id: str, user_message: str, response_data: Dict[str, Any]):
        """
        Save conversation to database.

        Args:
            thread_id: Thread identifier
            user_message: User's message
            response_data: Response data
        """
        try:
            db = get_db()
            session_repo = ChatSessionRepository(db)

            # Save user message
            await session_repo.add_message(
                thread_id=thread_id,
                role="user",
                content=user_message
            )

            # Save assistant response
            await session_repo.add_message(
                thread_id=thread_id,
                role="assistant",
                content=response_data["response"],
                metadata={
                    "intent": response_data.get("intent"),
                    "has_products": response_data.get("products") is not None,
                    "has_comparison": response_data.get("comparison") is not None,
                    "has_order": response_data.get("order_confirmation") is not None,
                }
            )

            logger.info(f"Saved conversation to database: {thread_id}")

        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            # Don't fail the request if database save fails

    async def get_session_history(self, thread_id: str) -> Dict[str, Any]:
        """
        Get conversation history for a thread.

        Args:
            thread_id: Thread identifier

        Returns:
            Dict with session data
        """
        try:
            db = get_db()
            session_repo = ChatSessionRepository(db)

            session = await session_repo.get_session_by_thread(thread_id)

            if not session:
                return {
                    "thread_id": thread_id,
                    "messages": [],
                    "error": "Session not found"
                }

            return {
                "thread_id": thread_id,
                "messages": [m.dict() for m in session.messages],
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting session history: {e}")
            return {
                "thread_id": thread_id,
                "messages": [],
                "error": str(e)
            }
