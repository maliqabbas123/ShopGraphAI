"""
FastAPI main application.

This module initializes and configures the FastAPI application.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging
from backend.app.db import MongoDB
from backend.app.api.v1 import api_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("ShopGraph AI Backend Starting...")
    logger.info("=" * 60)

    # Connect to MongoDB
    await MongoDB.connect_db()

    logger.info("Application startup complete")
    logger.info("=" * 60)

    yield

    # Shutdown
    logger.info("=" * 60)
    logger.info("ShopGraph AI Backend Shutting down...")
    logger.info("=" * 60)

    # Close MongoDB connection
    await MongoDB.close_db()

    logger.info("Application shutdown complete")
    logger.info("=" * 60)


# Create FastAPI app
app = FastAPI(
    title="ShopGraph AI",
    description="AI Shopping Assistant powered by LangGraph",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to ShopGraph AI",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "shopgraph-ai"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True if settings.environment == "development" else False
    )
