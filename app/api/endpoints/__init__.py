# File: /fastapi-app/fastapi-app/app/api/endpoints/__init__.py

from fastapi import APIRouter

router = APIRouter()

from .items import router as items_router
from .users import router as users_router

router.include_router(items_router, prefix="/items", tags=["items"])
router.include_router(users_router, prefix="/users", tags=["users"])