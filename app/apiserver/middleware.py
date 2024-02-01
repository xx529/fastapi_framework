import uuid

from starlette.requests import Request

from .context import RequestCtx
from .logger import middleware_log, request_start_log, request_finish_log


class MiddleWare:

    @staticmethod
    async def set_ctx(request: Request, call_next):
        RequestCtx.set_request_id(uuid.uuid4())
        middleware_log.debug(f'set request id: {RequestCtx.get_request_id()}')
        response = await call_next(request)
        return response

    @staticmethod
    async def log_request(request: Request, call_next):
        request_start_log.info(f'{request.method} {request.url}')
        middleware_log.debug(f'headers: {dict(request.headers)}')
        response = await call_next(request)
        request_finish_log.info(f'status code: {response.status_code}')
        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.set_ctx, cls.log_request]
        return mls[::-1]
