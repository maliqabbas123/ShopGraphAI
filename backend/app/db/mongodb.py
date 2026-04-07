"""
MongoDB database connection and client management.

This module handles the MongoDB connection lifecycle and provides
access to database collections.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """
    MongoDB connection manager.

    Provides singleton access to MongoDB client and database.
    Handles connection lifecycle (connect/disconnect).
    """

    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect_db(cls) -> None:
        """
        Establish connection to MongoDB.

        Creates client and selects database based on settings.
        Should be called on application startup.
        """
        try:
            logger.info(f"Connecting to MongoDB at {settings.mongodb_uri}")
            cls.client = AsyncIOMotorClient(settings.mongodb_uri)
            cls.database = cls.client[settings.database_name]

            # Verify connection
            await cls.client.admin.command("ping")
            logger.info(f"Successfully connected to MongoDB database: {settings.database_name}")

            # Create indexes
            await cls.create_indexes()

        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def close_db(cls) -> None:
        """
        Close MongoDB connection.

        Should be called on application shutdown.
        """
        if cls.client is not None:
            cls.client.close()
            logger.info("MongoDB connection closed")

    @classmethod
    async def create_indexes(cls) -> None:
        """
        Create database indexes for optimal query performance.

        Indexes are created on frequently queried fields.
        """
        if cls.database is None:
            return

        try:
            # Products collection indexes
            await cls.database.products.create_index("category")
            await cls.database.products.create_index("brand")
            await cls.database.products.create_index("price")
            await cls.database.products.create_index("rating")
            await cls.database.products.create_index([("title", "text")])

            # Chat sessions index
            await cls.database.chat_sessions.create_index("thread_id", unique=True)
            await cls.database.chat_sessions.create_index("created_at")

            # Carts index
            await cls.database.carts.create_index("user_id")

            # Orders index
            await cls.database.orders.create_index("order_id", unique=True)
            await cls.database.orders.create_index("user_id")

            logger.info("Database indexes created successfully")

        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """
        Get the database instance.

        Returns:
            Motor database instance

        Raises:
            RuntimeError: If database connection not established
        """
        if cls.database is None:
            raise RuntimeError("Database not connected. Call connect_db() first.")
        return cls.database


# Convenience function to get database
def get_db() -> AsyncIOMotorDatabase:
    """Get database instance."""
    return MongoDB.get_database()
