"""
Order and cart management tools.

Tools for adding to cart, checking stock, and placing orders.
"""

import logging
from typing import Dict, Any
from langchain.tools import tool
from datetime import datetime

logger = logging.getLogger(__name__)


@tool
async def check_stock_tool(product_id: str) -> Dict[str, Any]:
    """
    Check if a product is in stock.

    Args:
        product_id: Product ID to check

    Returns:
        Dict with stock availability information
    """
    try:
        from backend.app.repositories.product_repository import ProductRepository
        from backend.app.db import get_db

        logger.info(f"Checking stock for product: {product_id}")

        db = get_db()
        repo = ProductRepository(db)

        product = await repo.get_product_by_id(product_id)

        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }

        in_stock = product.stock > 0

        logger.info(f"Product {product_id}: stock={product.stock}, in_stock={in_stock}")

        return {
            "success": True,
            "product_id": product_id,
            "in_stock": in_stock,
            "stock_quantity": product.stock,
            "product_title": product.title,
            "price": product.price
        }

    except Exception as e:
        logger.error(f"Error in check_stock_tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@tool
async def add_to_cart_tool(product_id: str, quantity: int = 1, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Add a product to the shopping cart.

    Args:
        product_id: Product ID to add
        quantity: Quantity to add (default 1)
        user_id: User identifier

    Returns:
        Dict with cart update status
    """
    try:
        from backend.app.repositories.cart_repository import CartRepository
        from backend.app.repositories.product_repository import ProductRepository
        from backend.app.db import get_db

        logger.info(f"Adding product {product_id} (qty: {quantity}) to cart for user {user_id}")

        db = get_db()
        product_repo = ProductRepository(db)
        cart_repo = CartRepository(db)

        # Verify product exists and is in stock
        product = await product_repo.get_product_by_id(product_id)
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }

        if product.stock < quantity:
            return {
                "success": False,
                "error": f"Insufficient stock. Only {product.stock} available."
            }

        # Add to cart
        cart = await cart_repo.add_item(user_id, product_id, quantity)

        logger.info(f"Product added to cart successfully")

        return {
            "success": True,
            "cart_id": cart.id,
            "product_title": product.title,
            "quantity": quantity,
            "total_items": len(cart.items)
        }

    except Exception as e:
        logger.error(f"Error in add_to_cart_tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@tool
async def place_order_tool(product_id: str, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Place an order for a single product (direct buy).

    Args:
        product_id: Product ID to order
        user_id: User identifier

    Returns:
        Dict with order confirmation details
    """
    try:
        from backend.app.repositories.order_repository import OrderRepository
        from backend.app.repositories.product_repository import ProductRepository
        from backend.app.db import get_db
        from backend.app.models import OrderItem
        import uuid

        logger.info(f"Placing order for product {product_id} for user {user_id}")

        db = get_db()
        product_repo = ProductRepository(db)
        order_repo = OrderRepository(db)

        # Get product
        product = await product_repo.get_product_by_id(product_id)
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }

        # Check stock
        if product.stock < 1:
            return {
                "success": False,
                "error": "Product out of stock"
            }

        # Create order
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

        order_item = OrderItem(
            product_id=product.id,
            product_title=product.title,
            quantity=1,
            price_at_purchase=product.price
        )

        order = await order_repo.create_order(
            order_id=order_id,
            user_id=user_id,
            items=[order_item],
            total_amount=product.price
        )

        # Update stock (decrement by 1)
        await product_repo.update_stock(product_id, product.stock - 1)

        logger.info(f"Order placed successfully: {order_id}")

        return {
            "success": True,
            "order_id": order_id,
            "product_title": product.title,
            "total_amount": product.price,
            "currency": product.currency,
            "status": "confirmed",
            "message": f"Order {order_id} placed successfully!"
        }

    except Exception as e:
        logger.error(f"Error in place_order_tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }
