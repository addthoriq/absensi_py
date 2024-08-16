from fastapi import APIRouter
from .auth import router as AuthRouter

routers = APIRouter()
routers.include_router(AuthRouter)
