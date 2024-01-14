from enum import Enum


class PullDataFormat(str, Enum):
    RAW = 'RAW'
    PANDAS = 'PANDAS',
    RECORDS = 'RECORDS'
    PYDANTIC = 'PYDANTIC'


class RedisKeyField(str, Enum):
    base = 'base'


class OrderTypeEnum(str, Enum):
    asc = 'asc'
    desc = 'desc'


class RequestSuccessCode(int, Enum):
    success = 200
    created = 201

    @classmethod
    def list(cls):
        return [x.value for x in list(cls)]
