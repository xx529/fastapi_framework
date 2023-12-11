import threading
import uuid


class MiddleWare:

    @staticmethod
    async def rename_thread(request, call_next):
        threading.current_thread().name = uuid.uuid4().hex
        response = await call_next(request)
        return response

    @staticmethod
    async def auth_handler(request, call_next):
        response = await call_next(request)
        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.rename_thread, cls.auth_handler]
        return mls[::-1]
