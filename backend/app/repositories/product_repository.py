"""
Product repository.

Data access layer for products collection.
Handles all MongoDB operations for products.
"""

import logging
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.app.models import Product

logger = logging.getLogger(__name__)


class ProductRepository:
    """
    Repository for product data access.

    Pure data layer - no business logic.
    """

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize repository.

        Args:
            database: MongoDB database instance
        """
        self.db = database
        self.collection = database.products

    async def search_products(self, filters: Dict[str, Any]) -> List[Product]:
        """
        Search products with filters.

        Args:
            filters: Dict of filter criteria
                - category: str
                - brand: str
                - min_price: float
                - max_price: float
                - min_rating: float
                - tags: List[str]

        Returns:
            List of matching products
        """
        query = {}

        # Category filter
        if "category" in filters:
            query["category"] = {"$regex": filters["category"], "$options": "i"}

        # Brand filter
        if "brand" in filters:
            query["brand"] = {"$regex": filters["brand"], "$options": "i"}

        # Price range filter
        if "min_price" in filters or "max_price" in filters:
            query["price"] = {}
            if "min_price" in filters:
                query["price"]["$gte"] = filters["min_price"]
            if "max_price" in filters:
                query["price"]["$lte"] = filters["max_price"]

        # Rating filter
        if "min_rating" in filters:
            query["rating"] = {"$gte": filters["min_rating"]}

        # Tags filter (match any tag)
        if "tags" in filters:
            query["tags"] = {"$in": filters["tags"]}

        logger.info(f"Product search query: {query}")

        # Execute query
        cursor = self.collection.find(query).limit(20)  # Limit to 20 results
        documents = await cursor.to_list(length=20)

        # Convert to Product models
        products = [Product(**doc) for doc in documents]

        logger.info(f"Found {len(products)} products")

        return products

    async def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """
        Get a single product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product or None if not found
        """
        document = await self.collection.find_one({"_id": product_id})

        if document:
            return Product(**document)

        return None

    async def get_products_by_ids(self, product_ids: List[str]) -> List[Product]:
        """
        Get multiple products by IDs.

        Args:
            product_ids: List of product IDs

        Returns:
            List of products
        """
        cursor = self.collection.find({"_id": {"$in": product_ids}})
        documents = await cursor.to_list(length=len(product_ids))

        products = [Product(**doc) for doc in documents]

        return products

    async def update_stock(self, product_id: str, new_stock: int) -> bool:
        """
        Update product stock quantity.

        Args:
            product_id: Product ID
            new_stock: New stock quantity

        Returns:
            True if updated, False otherwise
        """
        result = await self.collection.update_one(
            {"_id": product_id},
            {"$set": {"stock": new_stock}}
        )

        return result.modified_count > 0

    async def get_all_products(self, limit: int = 100) -> List[Product]:
        """
        Get all products (with limit).

        Args:
            limit: Maximum number of products to return

        Returns:
            List of products
        """
        cursor = self.collection.find().limit(limit)
        documents = await cursor.to_list(length=limit)

        products = [Product(**doc) for doc in documents]

        return products
