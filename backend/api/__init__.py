from fastapi import APIRouter
from backend.api import health, posts, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(posts.router, prefix="/api/posts", tags=["posts"])
api_router.include_router(ui.router, tags=["ui"])
