from enum import Enum

from app.config import kafka_conf


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

    @classmethod
    def note(cls):
        return (f'升序（{cls.ASC.value})；'
                f'降序（{cls.DESC.value})；')


class LoggerNameEnum(str, Enum):
    RUNTIME = 'runtime'
    LIFESPAN = 'lifespan'
    SQL = 'sql'
    KAFKA = 'kafka'
    REDIS = 'redis'
    MIDDLEWARE = 'middleware'
    REQUEST_START = 'request_start'
    REQUEST_FINISH = 'request_finish'
    TRANSACTION = 'transaction'
    EXCEPTION = 'exception'


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


class HumanGender(str, Enum):
    FEMALE = '女'
    MALE = '男'


class KafkaTopic(str, Enum):
    chat_task = kafka_conf.topics['chat_task'].topic_name
    log_task = kafka_conf.topics['log_task'].topic_name
