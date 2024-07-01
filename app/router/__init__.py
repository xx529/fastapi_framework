from fastapi import APIRouter

from app.router import (
    stream_router,
    system_router,
    task_router,
    user_router,
)

routers = APIRouter()
routers.include_router()
routers.include_router(task_router.router)
routers.include_router(user_router.router)
routers.include_router(stream_router.router)
routers.include_router(system_router.router)

all_routers = [
    task_router.router,
    user_router.router,
    stream_router.router,
    system_router.router,
]
