import threading
import uuid
from starlette.requests import Request
from .logger import request_logger


class MiddleWare:

    @staticmethod
    async def show_request_info(request: Request, call_next):
        request_logger.debug(f'{request.method} {request.url}')
        request_logger.debug(f'headers: {dict(request.headers)}')
        response = await call_next(request)
        if response.status_code not in [200]:
            request_logger.error(f'{response.status_code}')
        else:
            request_logger.info(f'{response.status_code}')
        return response

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
        mls = [cls.rename_thread, cls.show_request_info, cls.auth_handler]
        return mls[::-1]
