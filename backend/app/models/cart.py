"""
Shopping cart data models.
"""

from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class CartItem(BaseModel):
    """Single item in a shopping cart."""

    product_id: str
    quantity: int = 1
    added_at: datetime = Field(default_factory=datetime.utcnow)


class Cart(BaseModel):
    """
    Shopping cart model.

    Stores user's selected items before checkout.
    """

    id: str = Field(alias="_id")
    user_id: str = "default_user"  # Mock user for now
    items: List[CartItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
