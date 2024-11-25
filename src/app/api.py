from fastapi import APIRouter

from .auth.views import auth_router
from .user.views import user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/user", tags=["User"])
