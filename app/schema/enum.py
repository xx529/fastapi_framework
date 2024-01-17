from enum import Enum


class PullDataFormat(str, Enum):
    RAW = 'raw'
    PANDAS = 'pandas',
    RECORDS = 'records'
    PYDANTIC = 'pydantic'


class RedisKeyField(str, Enum):
    BASE = 'base'


class OrderTypeEnum(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class RequestSuccessCode(int, Enum):
    SUCCESS = 200
    CREATED = 201

    @classmethod
    def list(cls):
        return [x.value for x in list(cls)]


class LoggerType(str, Enum):
    RUNTIME = 'runtime'
    LIFESPAN = 'lifespan'
    DATABASE = 'database'
    REDIS = 'redis'


class RedisKey(str, Enum):
    USER_REPO = 'user_repo'
    ITEM_REPO = 'item_repo'
