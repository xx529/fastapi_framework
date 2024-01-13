from starlette.requests import Request
import uuid
from .logger import request_logger
from .context import RequestCtx


class MiddleWare:

    @staticmethod
    async def set_ctx(request: Request, call_next):
        RequestCtx.set_request_id(uuid.uuid4())
        response = await call_next(request)
        return response

    @staticmethod
    async def show_request_info(request: Request, call_next):
        request_logger.info(f'{request.method} {request.url}')
        request_logger.debug(f'headers: {dict(request.headers)}')
        response = await call_next(request)
        if response.status_code not in [200]:
            request_logger.error(f'{response.status_code}')
        else:
            request_logger.info(f'{response.status_code}')
        return response

    @staticmethod
    async def auth_handler(request, call_next):
        response = await call_next(request)
        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.set_ctx, cls.show_request_info, cls.auth_handler]
        return mls[::-1]
