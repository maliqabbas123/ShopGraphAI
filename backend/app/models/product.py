"""
Product data models.

Defines the structure of product documents in MongoDB.
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Product(BaseModel):
    """
    Product model representing an item in the catalog.

    This model is used both for MongoDB documents and
    in-memory product representations.
    """

    id: str = Field(alias="_id")
    title: str
    brand: str
    category: str
    description: str
    price: float
    currency: str = "USD"
    rating: float
    stock: int
    attributes: Dict[str, str] = Field(default_factory=dict)  # Specs like RAM, storage, etc.
    tags: List[str] = Field(default_factory=list)  # Searchable tags
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "prod_001",
                "title": "Gaming Laptop Pro X",
                "brand": "TechBrand",
                "category": "laptop",
                "description": "High-performance gaming laptop with RTX 4070",
                "price": 1299.99,
                "currency": "USD",
                "rating": 4.5,
                "stock": 15,
                "attributes": {
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "processor": "Intel i7-13700H",
                    "gpu": "RTX 4070"
                },
                "tags": ["gaming", "laptop", "high-performance"]
            }
        }
