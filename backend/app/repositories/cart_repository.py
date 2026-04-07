"""
Cart repository.

Data access layer for shopping carts.
"""

import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from backend.app.models import Cart, CartItem

logger = logging.getLogger(__name__)


class CartRepository:
    """
    Repository for cart data access.
    """

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize repository.

        Args:
            database: MongoDB database instance
        """
        self.db = database
        self.collection = database.carts

    async def get_or_create_cart(self, user_id: str) -> Cart:
        """
        Get user's cart or create if doesn't exist.

        Args:
            user_id: User identifier

        Returns:
            User's cart
        """
        document = await self.collection.find_one({"user_id": user_id})

        if document:
            return Cart(**document)

        # Create new cart
        cart_id = f"cart_{user_id}_{int(datetime.utcnow().timestamp())}"
        new_cart = Cart(
            _id=cart_id,
            user_id=user_id,
            items=[],
        )

        await self.collection.insert_one(new_cart.dict(by_alias=True))

        logger.info(f"Created new cart: {cart_id}")

        return new_cart

    async def add_item(self, user_id: str, product_id: str, quantity: int = 1) -> Cart:
        """
        Add item to cart.

        Args:
            user_id: User identifier
            product_id: Product ID to add
            quantity: Quantity to add

        Returns:
            Updated cart
        """
        cart = await self.get_or_create_cart(user_id)

        # Check if item already in cart
        existing_item = None
        for item in cart.items:
            if item.product_id == product_id:
                existing_item = item
                break

        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
        else:
            # Add new item
            cart.items.append(CartItem(product_id=product_id, quantity=quantity))

        cart.updated_at = datetime.utcnow()

        # Update in database
        await self.collection.update_one(
            {"_id": cart.id},
            {"$set": cart.dict(by_alias=True, exclude={"id"})}
        )

        logger.info(f"Added {quantity}x {product_id} to cart {cart.id}")

        return cart

    async def remove_item(self, user_id: str, product_id: str) -> Cart:
        """
        Remove item from cart.

        Args:
            user_id: User identifier
            product_id: Product ID to remove

        Returns:
            Updated cart
        """
        cart = await self.get_or_create_cart(user_id)

        cart.items = [item for item in cart.items if item.product_id != product_id]
        cart.updated_at = datetime.utcnow()

        await self.collection.update_one(
            {"_id": cart.id},
            {"$set": cart.dict(by_alias=True, exclude={"id"})}
        )

        logger.info(f"Removed {product_id} from cart {cart.id}")

        return cart

    async def clear_cart(self, user_id: str) -> Cart:
        """
        Clear all items from cart.

        Args:
            user_id: User identifier

        Returns:
            Empty cart
        """
        cart = await self.get_or_create_cart(user_id)

        cart.items = []
        cart.updated_at = datetime.utcnow()

        await self.collection.update_one(
            {"_id": cart.id},
            {"$set": cart.dict(by_alias=True, exclude={"id"})}
        )

        logger.info(f"Cleared cart {cart.id}")

        return cart
