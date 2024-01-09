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
