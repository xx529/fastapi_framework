from enum import Enum

from pydantic import BaseModel


class ErrorMsg(BaseModel):
    errcode: int
    errmsg: str
    status_code: int = 400


class AppExceptionClass(Exception):

    def __init__(self, detail: str, errmsg: str, errcode: int, status_code: int):
        self.detail = detail
        self.errmsg = errmsg
        self.errcode = errcode
        self.status_code = status_code


class AppException(Enum):
    Unknown = ErrorMsg(errcode=10000, errmsg='未知错误')
    Runtime = ErrorMsg(errcode=10001, errmsg='运行时错误')
    Demo = ErrorMsg(errcode=9999, errmsg='demo问题')
    Random = ErrorMsg(errcode=9998, errmsg='随机报错')
    InvalidPathParameter = ErrorMsg(errcode=9997, errmsg='路由参数错误')
    InvalidHeaderParameter = ErrorMsg(errcode=9997, errmsg='请求头参数错误')
    InvalidBodyParameter = ErrorMsg(errcode=9997, errmsg='请求体错误')

    def __call__(self, detail) -> AppExceptionClass:
        return AppExceptionClass(detail=detail,
                                 errmsg=self.value.errmsg,
                                 errcode=self.value.errcode,
                                 status_code=self.value.status_code)
