"""
Database seeding script.

Populates MongoDB with sample product data for testing.

Usage (from root directory):
    python seed_database.py
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_database():
    """
    Seed the database with sample product data.
    """
    logger.info("=" * 60)
    logger.info("Starting database seeding...")
    logger.info("=" * 60)

    # Connect to MongoDB
    logger.info(f"Connecting to MongoDB: {settings.mongodb_uri}")
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]

    try:
        # Load seed data
        seed_file = Path(__file__).parent / "scripts" / "seed_data.json"
        logger.info(f"Loading seed data from: {seed_file}")

        with open(seed_file, "r") as f:
            products_data = json.load(f)

        logger.info(f"Loaded {len(products_data)} products")

        # Clear existing products
        logger.info("Clearing existing products collection...")
        await db.products.delete_many({})
        logger.info("✓ Products collection cleared")

        # Insert products
        logger.info("Inserting products...")
        result = await db.products.insert_many(products_data)
        logger.info(f"✓ Inserted {len(result.inserted_ids)} products")

        # Create indexes
        logger.info("Creating indexes...")
        await db.products.create_index("category")
        await db.products.create_index("brand")
        await db.products.create_index("price")
        await db.products.create_index("rating")
        await db.products.create_index([("title", "text")])
        logger.info("✓ Indexes created")

        # Display summary
        logger.info("=" * 60)
        logger.info("Seeding Summary:")
        logger.info("=" * 60)

        categories = await db.products.distinct("category")
        logger.info(f"Categories: {', '.join(categories)}")

        for category in categories:
            count = await db.products.count_documents({"category": category})
            logger.info(f"  - {category}: {count} products")

        brands = await db.products.distinct("brand")
        logger.info(f"Brands: {', '.join(brands)}")

        logger.info("=" * 60)
        logger.info("✓ Database seeding completed successfully!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error seeding database: {e}", exc_info=True)
        raise

    finally:
        client.close()
        logger.info("MongoDB connection closed")


if __name__ == "__main__":
    asyncio.run(seed_database())
