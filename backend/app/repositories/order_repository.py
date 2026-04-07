"""
Order repository.

Data access layer for orders.
"""

import logging
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from backend.app.models import Order, OrderItem, OrderStatus

logger = logging.getLogger(__name__)


class OrderRepository:
    """
    Repository for order data access.
    """

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize repository.

        Args:
            database: MongoDB database instance
        """
        self.db = database
        self.collection = database.orders

    async def create_order(
        self,
        order_id: str,
        user_id: str,
        items: List[OrderItem],
        total_amount: float,
        currency: str = "USD"
    ) -> Order:
        """
        Create a new order.

        Args:
            order_id: Unique order ID
            user_id: User identifier
            items: List of order items
            total_amount: Total order amount
            currency: Currency code

        Returns:
            Created order
        """
        doc_id = f"order_{int(datetime.utcnow().timestamp())}_{user_id}"

        order = Order(
            _id=doc_id,
            order_id=order_id,
            user_id=user_id,
            items=items,
            total_amount=total_amount,
            currency=currency,
            status=OrderStatus.CONFIRMED,
        )

        await self.collection.insert_one(order.dict(by_alias=True))

        logger.info(f"Created order: {order_id}")

        return order

    async def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """
        Get order by order ID.

        Args:
            order_id: Order ID

        Returns:
            Order or None if not found
        """
        document = await self.collection.find_one({"order_id": order_id})

        if document:
            return Order(**document)

        return None

    async def get_orders_by_user(self, user_id: str, limit: int = 10) -> List[Order]:
        """
        Get user's orders.

        Args:
            user_id: User identifier
            limit: Maximum number of orders to return

        Returns:
            List of orders
        """
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        documents = await cursor.to_list(length=limit)

        orders = [Order(**doc) for doc in documents]

        return orders

    async def update_order_status(self, order_id: str, status: OrderStatus) -> bool:
        """
        Update order status.

        Args:
            order_id: Order ID
            status: New status

        Returns:
            True if updated, False otherwise
        """
        result = await self.collection.update_one(
            {"order_id": order_id},
            {
                "$set": {
                    "status": status.value,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        return result.modified_count > 0
