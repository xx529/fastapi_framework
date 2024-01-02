from app.router import system_router
from app.router import user_router
from app.router import stream_router


all_routers = [
    system_router.router,
    user_router.router,
    stream_router.router,
]
