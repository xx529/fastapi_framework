from enum import Enum


class PullDataFormatEnum(str, Enum):
    RAW = 'raw'
    PANDAS = 'pandas',
    RECORDS = 'records'
    NULL = 'null'


class OrderTypeEnum(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class RequestSuccessCodeEnum(int, Enum):
    SUCCESS = 200
    CREATED = 201

    @classmethod
    def list(cls):
        return [x.value for x in list(cls)]


class LoggerTypeEnum(str, Enum):
    RUNTIME = 'runtime'
    LIFESPAN = 'lifespan'
    POSTGRES = 'postgres'
    REDIS = 'redis'


class RedisKeyEnum(str, Enum):
    USER_REPO = 'user_repo'
    ITEM_REPO = 'item_repo'
