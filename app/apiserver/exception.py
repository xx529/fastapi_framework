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
    Unknown = ErrorMsg(errcode=9999, errmsg='未知错误')

    SystemError = ErrorMsg(errcode=1000, errmsg='系统错误')
    RuntimeError = ErrorMsg(errcode=1001, errmsg='运行时错误')
    DatabaseError = ErrorMsg(errcode=1002, errmsg='数据库错误')
    RemoteCallError = ErrorMsg(errcode=1003, errmsg='远程调用错误')

    InvalidError = ErrorMsg(errcode=2000, errmsg='参数错误')
    InvalidPathParameter = ErrorMsg(errcode=2001, errmsg='路由参数错误')
    InvalidHeaderParameter = ErrorMsg(errcode=2002, errmsg='请求头参数错误')
    InvalidBodyParameter = ErrorMsg(errcode=2003, errmsg='请求体错误')

    UserNotExist = ErrorMsg(errcode=3001, errmsg='用户不存在')
    Demo = ErrorMsg(errcode=3000, errmsg='demo问题')
    Random = ErrorMsg(errcode=3001, errmsg='随机报错')

    def __call__(self, detail='') -> AppExceptionClass:
        return AppExceptionClass(detail=detail,
                                 errmsg=self.value.errmsg,
                                 errcode=self.value.errcode,
                                 status_code=self.value.status_code)
