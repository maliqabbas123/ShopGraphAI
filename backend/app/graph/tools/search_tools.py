"""
Product search tools.

These tools are called by the search subgraph to find and filter products.
"""

import logging
from typing import Dict, Any, Optional, List
from langchain.tools import tool

# Import will be added after repositories are created
# For now, we'll create placeholder that will be replaced

logger = logging.getLogger(__name__)


@tool
async def search_products_tool(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Search for products based on filters.

    This tool queries the product database with specified filters.
    Multiple filters can be combined for refined search.

    Args:
        category: Product category (laptop, phone, headphones, etc.)
        brand: Brand name (Apple, Samsung, Dell, etc.)
        min_price: Minimum price in USD
        max_price: Maximum price in USD
        min_rating: Minimum rating (1-5)
        tags: List of tags to match (gaming, wireless, etc.)

    Returns:
        Dict with 'success', 'products' list, and optional 'error'
    """
    try:
        # Import here to avoid circular dependency
        from backend.app.repositories.product_repository import ProductRepository
        from backend.app.db import get_db

        logger.info(f"Searching products with filters: category={category}, brand={brand}, "
                   f"price={min_price}-{max_price}, rating={min_rating}, tags={tags}")

        db = get_db()
        repo = ProductRepository(db)

        # Build filter dict
        filters = {}
        if category:
            filters["category"] = category
        if brand:
            filters["brand"] = brand
        if min_price is not None:
            filters["min_price"] = min_price
        if max_price is not None:
            filters["max_price"] = max_price
        if min_rating is not None:
            filters["min_rating"] = min_rating
        if tags:
            filters["tags"] = tags

        # Search products
        products = await repo.search_products(filters)

        logger.info(f"Found {len(products)} products")

        return {
            "success": True,
            "products": [p.dict(by_alias=True) for p in products],
            "count": len(products)
        }

    except Exception as e:
        logger.error(f"Error in search_products_tool: {e}")
        return {
            "success": False,
            "products": [],
            "error": str(e)
        }


@tool
async def filter_products_tool(
    product_ids: List[str],
    brand: Optional[str] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Filter existing products by additional criteria.

    Used for refining search results when user adds more constraints.

    Args:
        product_ids: List of product IDs to filter
        brand: Filter by brand
        max_price: Filter by maximum price
        min_rating: Filter by minimum rating

    Returns:
        Dict with filtered products
    """
    try:
        from backend.app.repositories.product_repository import ProductRepository
        from backend.app.db import get_db

        logger.info(f"Filtering {len(product_ids)} products")

        db = get_db()
        repo = ProductRepository(db)

        # Get products by IDs
        products = await repo.get_products_by_ids(product_ids)

        # Apply filters
        filtered = products
        if brand:
            filtered = [p for p in filtered if p.brand.lower() == brand.lower()]
        if max_price is not None:
            filtered = [p for p in filtered if p.price <= max_price]
        if min_rating is not None:
            filtered = [p for p in filtered if p.rating >= min_rating]

        logger.info(f"Filtered to {len(filtered)} products")

        return {
            "success": True,
            "products": [p.dict(by_alias=True) for p in filtered],
            "count": len(filtered)
        }

    except Exception as e:
        logger.error(f"Error in filter_products_tool: {e}")
        return {
            "success": False,
            "products": [],
            "error": str(e)
        }
