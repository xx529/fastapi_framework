import json

from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.apiserver import AppExceptionEnum
from app.apiserver.exception import AppError
from app.schema.response.base import BaseResponse


class ExceptionHandler:

    @staticmethod
    async def request_exception_handler(r: Request, e: RequestValidationError):
        logger.error(r)
        logger.error('\n' + json.dumps(e.errors(), indent=4))
        detail = ''.join([f"{str(err.get('loc'))}:{err.get('msg')};" for err in e.errors()])
        err = AppExceptionEnum.InvalidError(detail=detail)
        resp = BaseResponse(errcode=err.errcode, errmsg=err.errmsg, detail=detail, data={}).model_dump()
        return JSONResponse(status_code=200, content=resp)

    @staticmethod
    async def app_exception_handler(r: Request, e: AppError):
        logger.error(r)
        logger.error('\n' + json.dumps(e.to_dict(), indent=4))
        resp = BaseResponse(errcode=e.errcode, errmsg=e.errmsg, detail=e.detail, data={}).model_dump()
        return JSONResponse(status_code=200, content=resp)
