from app.router import system_router
from app.router import user_router


all_routers = [
    system_router.router,
    user_router.router,
]
