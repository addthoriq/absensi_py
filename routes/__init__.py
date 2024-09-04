from fastapi import APIRouter
from .auth import router as AuthRouter
from .user import router as UserRouter
from .jabatan import router as JabatanRouter
from .shift import router as ShiftRouter

routers = APIRouter()
routers.include_router(AuthRouter)
routers.include_router(UserRouter)
routers.include_router(JabatanRouter)
routers.include_router(ShiftRouter)