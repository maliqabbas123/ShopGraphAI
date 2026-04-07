"""
Chat API request/response schemas.

Pydantic models for validating chat endpoint payloads.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """Request schema for sending a chat message."""

    message: str = Field(..., min_length=1, max_length=1000)
    thread_id: Optional[str] = None  # If None, creates new session

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Find me gaming laptops under $1500",
                "thread_id": "thread_abc123"
            }
        }


class ProductInfo(BaseModel):
    """Product information in chat response."""

    id: str
    title: str
    brand: str
    price: float
    rating: float
    stock: int
    category: str
    attributes: Dict[str, str] = Field(default_factory=dict)


class ChatMessageResponse(BaseModel):
    """Response schema for chat message."""

    thread_id: str
    response: str
    products: Optional[List[ProductInfo]] = None
    comparison: Optional[Dict[str, Any]] = None
    order_confirmation: Optional[Dict[str, Any]] = None
    intent: Optional[str] = None  # Helpful for debugging

    class Config:
        json_schema_extra = {
            "example": {
                "thread_id": "thread_abc123",
                "response": "I found 5 gaming laptops under $1500. Here are the top options:",
                "products": [
                    {
                        "id": "prod_001",
                        "title": "Gaming Laptop Pro",
                        "brand": "TechBrand",
                        "price": 1299.99,
                        "rating": 4.5,
                        "stock": 10,
                        "category": "laptop",
                        "attributes": {"ram": "16GB", "storage": "512GB"}
                    }
                ],
                "intent": "search"
            }
        }


class ChatHistoryResponse(BaseModel):
    """Response schema for chat history retrieval."""

    thread_id: str
    messages: List[Dict[str, Any]]
    created_at: str
    updated_at: str
