from enum import Enum


class PullDataFormatEnum(str, Enum):
    RAW = 'raw'
    PANDAS = 'pandas',
    RECORDS = 'records'
    PYDANTIC = 'pydantic'


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
    DATABASE = 'database'
    REDIS = 'redis'


class RedisKeyEnum(str, Enum):
    USER_REPO = 'user_repo'
    ITEM_REPO = 'item_repo'


class RedisActionEnum(str, Enum):
    CACHE = 'cache'  # 自动缓存与查询
    CLEAR = 'clear'  # 删除行为对应的缓存
