__all__ = [
    'router',
]


from fastapi import APIRouter

from src.api.v1.routers import router_users

router = APIRouter()
router.include_router(router_users)
