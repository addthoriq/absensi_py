from fastapi import APIRouter
from .auth import router as AuthRouter
from .user import router as UserRouter

routers = APIRouter()
routers.include_router(AuthRouter)
routers.include_router(UserRouter)
