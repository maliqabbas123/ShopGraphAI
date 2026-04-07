"""
Frontend routes for serving React build.

Handles serving the Vite/React production build from frontend/dist.
This includes index.html and all static assets.
"""

import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# Frontend build directory path
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")

# Create router
router = APIRouter()


@router.get("/favicon.ico")
async def serve_favicon():
    """Serve favicon."""
    file_path = os.path.join(frontend_dist, "favicon.ico")
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # Fallback to vite.svg if favicon.ico doesn't exist
    vite_svg = os.path.join(frontend_dist, "vite.svg")
    if os.path.isfile(vite_svg):
        return FileResponse(vite_svg)
    raise HTTPException(status_code=404, detail="Favicon not found")


@router.get("/{path:path}")
async def serve_frontend(path: str = ""):
    """
    Serve the React SPA.

    For any non-API route, serve index.html.
    This enables client-side routing to work properly.
    """
    # Don't serve API routes here (they're handled by api_router)
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")

    # Check if a specific file is requested
    if path and "." in path.split("/")[-1]:
        # This looks like a file request (e.g., logo.png, robots.txt)
        file_path = os.path.join(frontend_dist, path)

        # Security: ensure path stays within frontend_dist
        if not os.path.abspath(file_path).startswith(os.path.abspath(frontend_dist)):
            raise HTTPException(status_code=404, detail="File not found")

        if os.path.isfile(file_path):
            return FileResponse(file_path)

        raise HTTPException(status_code=404, detail="File not found")

    # For all other routes (or root), serve index.html
    # This is how SPAs work - the client-side router handles the actual routing
    index_path = os.path.join(frontend_dist, "index.html")

    if os.path.isfile(index_path):
        return FileResponse(index_path, media_type="text/html")

    # If index.html doesn't exist, frontend hasn't been built
    raise HTTPException(
        status_code=503,
        detail="Frontend not built. Run 'npm run build' in the frontend directory."
    )
