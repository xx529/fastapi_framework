import random

from fastapi import HTTPException


class MyException:

    @classmethod
    def my_exception(cls):
        return HTTPException(status_code=400, detail='my exception')


class Depd:

    @staticmethod
    def error_dep():
        t = random.random()
        print(t)
        if t > 0.5:
            raise MyException.my_exception()
        return '1'
