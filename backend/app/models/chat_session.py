"""
Chat session data models.

Stores conversation history and state for each user session.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single message in a conversation."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None  # Optional metadata like product IDs, etc.


class ChatSession(BaseModel):
    """
    Chat session model.

    Stores complete conversation history and associated state
    for a user's interaction thread.
    """

    id: str = Field(alias="_id")
    thread_id: str  # Unique identifier for this conversation thread
    user_id: str = "default_user"
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Session state (optional fields to track context)
    last_search_results: Optional[List[str]] = None  # Product IDs from last search
    selected_products: Optional[List[str]] = None  # Currently selected product IDs

    class Config:
        populate_by_name = True
