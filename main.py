"""
ShopGraph AI - Main FastAPI application entry point.

This is the root entry point that serves both the API and the frontend.
Backend code is in backend/ directory, frontend build is served from frontend/dist.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging
from backend.app.db import MongoDB
from backend.app.api.v1 import api_router
from frontend_routes import router as frontend_router

# Setup logging first
setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # === STARTUP ===
    logger.info("=" * 60)
    logger.info("ShopGraph AI Backend Starting...")
    logger.info("=" * 60)

    # Connect to MongoDB
    await MongoDB.connect_db()

    logger.info("Application startup complete")
    logger.info("=" * 60)

    yield

    # === SHUTDOWN ===
    logger.info("=" * 60)
    logger.info("ShopGraph AI Backend Shutting down...")
    logger.info("=" * 60)

    # Close MongoDB connection
    await MongoDB.close_db()

    logger.info("Application shutdown complete")
    logger.info("=" * 60)


# Initialize FastAPI app
app = FastAPI(
    title="ShopGraph AI",
    description="AI Shopping Assistant powered by LangGraph",
    version="1.0.0",
    lifespan=lifespan,
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

# Serve frontend static files
# Check if frontend build exists
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.exists(frontend_dist):
    logger.info(f"Serving frontend from: {frontend_dist}")

    # Mount frontend static assets (JS, CSS, etc.)
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount(
            "/assets",
            StaticFiles(directory=assets_dir),
            name="assets",
        )

    # Include frontend router for HTML pages and other static files
    app.include_router(frontend_router)
else:
    logger.warning(f"Frontend build not found at {frontend_dist}")
    logger.warning("Run 'npm run build' in the frontend directory to build the frontend")


@app.get("/")
async def root():
    """Root endpoint - serves frontend if built, otherwise API info."""
    # If frontend exists, it will be served by frontend_routes.py
    # This is a fallback if frontend is not built
    return {
        "message": "ShopGraph AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "api": settings.api_v1_prefix,
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
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True if settings.environment == "development" else False
    )
