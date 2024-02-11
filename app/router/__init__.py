from app.router import (
    stream_router,
    system_router,
    task_router,
    user_router,
)

all_routers = [
    stream_router.router,
    system_router.router,
    task_router.router,
    user_router.router,
]
