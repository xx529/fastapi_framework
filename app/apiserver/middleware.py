import traceback
import uuid

from fastapi.responses import JSONResponse
from loguru import logger
from starlette.requests import Request

from app.schema.base import BaseResponse
from .exception import AppException, AppExceptionClass
from .logger import exception_log, middleware_log, request_finish_log, request_start_log


class MiddleWare:

    @staticmethod
    async def set_logger_trace_id(request: Request, call_next):

        trace_id = uuid.uuid4().hex
        with logger.contextualize(trace_id=trace_id):
            middleware_log.debug(f'set trace id: {trace_id}')
            response = await call_next(request)
            print(response.content)
            return response

    @staticmethod
    async def log_request(request: Request, call_next):
        request_start_log.info(f'{request.method} {request.url}')
        middleware_log.debug(f'headers: {dict(request.headers)}')

        try:
            response = await call_next(request)
            request_finish_log.info(f'status code: {response.status_code}')

        except AppExceptionClass as e:
            res = BaseResponse(errcode=e.errcode,
                               errmsg=e.errmsg,
                               detail=e.detail,
                               data='')
            response = JSONResponse(status_code=e.status_code,
                                    content=res.model_dump())
            exception_log.error(traceback.format_exc())
            request_finish_log.info(
                f'status code: {response.status_code} error code: {e.errcode} error msg: {e.errmsg} detail: {e.detail}')

        except Exception as e:
            res = BaseResponse(errcode=AppException.Unknown.value.errcode,
                               errmsg=AppException.Unknown.value.errmsg,
                               detail=AppException.Unknown.value.errmsg,
                               data='')
            response = JSONResponse(status_code=AppException.Unknown.value.status_code,
                                    content=res.model_dump())
            exception_log.error(traceback.format_exc())
            request_finish_log.info(
                f'status code: {response.status_code} error code: {AppException.Unknown.value.errcode} error msg: {type(e).__name__} detail: {str(e)}')

        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.set_logger_trace_id, cls.log_request]
        return mls[::-1]
