import uuid

from starlette.requests import Request

from app.schema.enum import RequestSuccessCodeEnum
from .context import RequestCtx
from .logger import middleware_log


class MiddleWare:

    @staticmethod
    async def set_ctx(request: Request, call_next):
        RequestCtx.set_request_id(uuid.uuid4())
        middleware_log.debug(f'set request id: {RequestCtx.get_request_id()}')
        response = await call_next(request)
        return response

    @staticmethod
    async def log_request(request: Request, call_next):
        # TODO 记录服务日志开始 request_log

        middleware_log.info(f'{request.method} {request.url}')
        middleware_log.debug(f'headers: {dict(request.headers)}')
        response = await call_next(request)

        if response.status_code in RequestSuccessCodeEnum.list():
            middleware_log.info(f'status code: {response.status_code}')
        else:
            middleware_log.error(f'status code: {response.status_code}')

        # TODO 记录服务日志结束 request_log
        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.set_ctx, cls.log_request]
        return mls[::-1]
