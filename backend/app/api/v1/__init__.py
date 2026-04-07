"""API v1 router."""

from fastapi import APIRouter
from backend.app.api.v1.endpoints import chat

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

__all__ = ["api_router"]
