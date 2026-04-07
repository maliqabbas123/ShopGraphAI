"""
Order data models.
"""

from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enum."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """Single item in an order."""

    product_id: str
    product_title: str
    quantity: int
    price_at_purchase: float


class Order(BaseModel):
    """
    Order model representing a completed purchase.

    Stores order details and status.
    """

    id: str = Field(alias="_id")
    order_id: str  # User-facing order ID (e.g., ORD-2024-001)
    user_id: str = "default_user"
    items: List[OrderItem]
    total_amount: float
    currency: str = "USD"
    status: OrderStatus = OrderStatus.CONFIRMED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        use_enum_values = True
