"""
Chat session repository.

Data access layer for chat sessions and conversation history.
"""

import logging
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from backend.app.models import ChatSession, ChatMessage

logger = logging.getLogger(__name__)


class ChatSessionRepository:
    """
    Repository for chat session data access.
    """

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize repository.

        Args:
            database: MongoDB database instance
        """
        self.db = database
        self.collection = database.chat_sessions

    async def get_or_create_session(self, thread_id: str, user_id: str = "default_user") -> ChatSession:
        """
        Get existing session or create new one.

        Args:
            thread_id: Thread identifier
            user_id: User identifier

        Returns:
            Chat session
        """
        document = await self.collection.find_one({"thread_id": thread_id})

        if document:
            return ChatSession(**document)

        # Create new session
        doc_id = f"session_{thread_id}"
        new_session = ChatSession(
            _id=doc_id,
            thread_id=thread_id,
            user_id=user_id,
            messages=[],
        )

        await self.collection.insert_one(new_session.dict(by_alias=True))

        logger.info(f"Created new chat session: {thread_id}")

        return new_session

    async def add_message(self, thread_id: str, role: str, content: str, metadata: Optional[dict] = None) -> ChatSession:
        """
        Add message to session.

        Args:
            thread_id: Thread identifier
            role: "user" or "assistant"
            content: Message content
            metadata: Optional metadata

        Returns:
            Updated session
        """
        session = await self.get_or_create_session(thread_id)

        message = ChatMessage(
            role=role,
            content=content,
            metadata=metadata
        )

        session.messages.append(message)
        session.updated_at = datetime.utcnow()

        await self.collection.update_one(
            {"thread_id": thread_id},
            {
                "$set": {
                    "messages": [m.dict() for m in session.messages],
                    "updated_at": session.updated_at
                }
            }
        )

        logger.info(f"Added {role} message to session {thread_id}")

        return session

    async def get_session_by_thread(self, thread_id: str) -> Optional[ChatSession]:
        """
        Get session by thread ID.

        Args:
            thread_id: Thread identifier

        Returns:
            Chat session or None
        """
        document = await self.collection.find_one({"thread_id": thread_id})

        if document:
            return ChatSession(**document)

        return None

    async def update_session_state(
        self,
        thread_id: str,
        last_search_results: Optional[List[str]] = None,
        selected_products: Optional[List[str]] = None
    ) -> ChatSession:
        """
        Update session state fields.

        Args:
            thread_id: Thread identifier
            last_search_results: Product IDs from last search
            selected_products: Currently selected product IDs

        Returns:
            Updated session
        """
        session = await self.get_or_create_session(thread_id)

        update_fields = {"updated_at": datetime.utcnow()}

        if last_search_results is not None:
            session.last_search_results = last_search_results
            update_fields["last_search_results"] = last_search_results

        if selected_products is not None:
            session.selected_products = selected_products
            update_fields["selected_products"] = selected_products

        await self.collection.update_one(
            {"thread_id": thread_id},
            {"$set": update_fields}
        )

        return session
