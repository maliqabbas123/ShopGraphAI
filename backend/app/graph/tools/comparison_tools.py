"""
Product comparison tools.

Tools for comparing multiple products side-by-side.
"""

import logging
from typing import Dict, Any, List
from langchain.tools import tool

logger = logging.getLogger(__name__)


@tool
async def compare_products_tool(product_ids: List[str]) -> Dict[str, Any]:
    """
    Compare multiple products and generate structured comparison data.

    Creates a side-by-side comparison of key attributes.

    Args:
        product_ids: List of product IDs to compare (2-5 products)

    Returns:
        Dict with comparison data including feature matrix and summary
    """
    try:
        from backend.app.repositories.product_repository import ProductRepository
        from backend.app.db import get_db

        if len(product_ids) < 2:
            return {
                "success": False,
                "error": "Need at least 2 products to compare"
            }

        if len(product_ids) > 5:
            return {
                "success": False,
                "error": "Can compare maximum 5 products at once"
            }

        logger.info(f"Comparing {len(product_ids)} products: {product_ids}")

        db = get_db()
        repo = ProductRepository(db)

        # Get products
        products = await repo.get_products_by_ids(product_ids)

        if len(products) == 0:
            return {
                "success": False,
                "error": "No products found with given IDs"
            }

        # Build comparison matrix
        comparison = {
            "products": [
                {
                    "id": p.id,
                    "title": p.title,
                    "brand": p.brand,
                    "price": p.price,
                    "rating": p.rating,
                    "stock": p.stock,
                    "attributes": p.attributes,
                }
                for p in products
            ],
            "comparison_fields": {
                "price": {
                    "values": {p.id: p.price for p in products},
                    "best": min(products, key=lambda x: x.price).id,
                    "worst": max(products, key=lambda x: x.price).id,
                },
                "rating": {
                    "values": {p.id: p.rating for p in products},
                    "best": max(products, key=lambda x: x.rating).id,
                    "worst": min(products, key=lambda x: x.rating).id,
                },
                "stock": {
                    "values": {p.id: p.stock for p in products},
                    "best": max(products, key=lambda x: x.stock).id,
                },
            },
            "summary": {
                "best_value": min(products, key=lambda x: x.price).id,
                "highest_rated": max(products, key=lambda x: x.rating).id,
                "price_range": f"${min(p.price for p in products):.2f} - ${max(p.price for p in products):.2f}",
            }
        }

        logger.info("Comparison generated successfully")

        return {
            "success": True,
            "comparison": comparison
        }

    except Exception as e:
        logger.error(f"Error in compare_products_tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }
