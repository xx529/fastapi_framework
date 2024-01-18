import sys

from loguru import logger

from app.config import log_conf, app_conf
from app.schema.enum import LoggerTypeEnum
from .context import RequestCtx

FULL_FORMAT = ('{time:YYYY-MM-DD HH:mm:ss.SSS} '
               '{extra[project_name]} '
               '[PID:{process}] '
               '[TID:{thread}] '
               '[{level}] '
               '[{file.path}:{function}:{line}] '
               '- '
               '[RID:{extra[request_id]}] '
               '[TYPE:{extra[type]}] '
               '{message}')

SHORT_FORMAT = ('[{time:HH:mm:ss.SSS}] '
                '[RID:{extra[request_id]}] '
                '[{level}] '
                '[TYPE:{extra[type]}] '
                '{message}')


def patch_request_id(record):
    record['extra'].update(request_id=RequestCtx.get_request_id())


logger.remove()

logger.add(sink=log_conf.file,
           format=FULL_FORMAT,
           level=log_conf.level,
           serialize=False)

logger.add(sink=sys.stdout,
           format=SHORT_FORMAT,
           level=log_conf.level)

_logger = logger.patch(patch_request_id).bind(project_name=app_conf.name)

runtime_log = _logger.bind(type=LoggerTypeEnum.RUNTIME.value)
lifespan_log = _logger.bind(type=LoggerTypeEnum.LIFESPAN.value)
database_log = _logger.bind(type=LoggerTypeEnum.DATABASE.value)
redis_log = _logger.bind(type=LoggerTypeEnum.REDIS.value)
