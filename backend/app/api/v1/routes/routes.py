from fastapi import APIRouter
from .roles import router as roles_router
from .resources import router as resources_router
from .users import router as users_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(roles_router, prefix="/roles", tags=["roles"])
router.include_router(resources_router, prefix="/resources", tags=["resources"])
router.include_router(users_router, prefix="/users", tags=["users"])
