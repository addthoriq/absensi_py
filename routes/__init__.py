from fastapi import APIRouter
from .auth import router as AuthRouter
from .user import router as UserRouter
from .jabatan import router as JabatanRouter
from .shift import router as ShiftRouter
from .kehadiran import router as KehadiranRouter
from .absensi import router as AbsensiRouter

routers = APIRouter()
routers.include_router(AuthRouter)
routers.include_router(UserRouter)
routers.include_router(JabatanRouter)
routers.include_router(ShiftRouter)
routers.include_router(KehadiranRouter)
routers.include_router(AbsensiRouter)