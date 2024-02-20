from enum import Enum


class RequestMethod(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class PullDataFormatEnum(str, Enum):
    RAW = 'raw'
    PANDAS = 'pandas',
    RECORDS = 'records'
    NULL = 'null'


class OrderTypeEnum(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class LoggerTypeEnum(str, Enum):
    RUNTIME = 'runtime'
    LIFESPAN = 'lifespan'
    POSTGRES = 'postgres'
    REDIS = 'redis'
    MIDDLEWARE = 'middleware'
    REQUEST_START = 'request_start'
    REQUEST_FINISH = 'request_finish'
    TRANSACTION = 'transaction'
    EXCEPTION = 'exception'

    @classmethod
    def get_running_types(cls):
        return [cls.RUNTIME.value,
                cls.POSTGRES.value,
                cls.REDIS.value,
                cls.MIDDLEWARE.value,
                cls.TRANSACTION.value,
                cls.EXCEPTION.value]

    @classmethod
    def get_request_types(cls):
        return [cls.REQUEST_START.value,
                cls.REQUEST_FINISH.value]


class RedisKeyEnum(str, Enum):
    USER_REPO = 'user_repo'
    ITEM_REPO = 'item_repo'
    TASK_REPO = 'task_repo'


class TaskStatus(str, Enum):
    ON = 'on'
    OFF = 'off'


class TaskCategory(str, Enum):
    NORMAL = 'normal'
    URGENT = 'urgent'
