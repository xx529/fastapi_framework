from enum import Enum
from app.schema.base import ExceptionMsg


class ExceptionType(Enum):
    Demo = ExceptionMsg(errcode=9999, errmsg='demo问题')
    Random = ExceptionMsg(errcode=9998, errmsg='随机报错')


class ServerException(Exception):

    def __init__(self, detail: str, errmsg: str, errcode: int, status_code: int = 400):
        self.detail = detail
        self.errmsg = errmsg
        self.errcode = errcode
        self.status_code = status_code

    @classmethod
    def demo(cls, detail: str):
        return cls(detail=detail,
                   errmsg=ExceptionType.Demo.value.errmsg,
                   errcode=ExceptionType.Demo.value.errcode)

    @classmethod
    def random(cls, detail: str):
        return cls(detail=detail,
                   errmsg=ExceptionType.Random.value.errmsg,
                   errcode=ExceptionType.Random.value.errcode)
