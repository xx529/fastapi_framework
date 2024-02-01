import sys

from loguru import logger

from app.config import log_conf, app_conf
from app.schema.enum import LoggerTypeEnum
from .context import RequestCtx

FULL_FORMAT = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> '
               '<red>{extra[project_name]}</red> '
               '[PID:{process}] '
               '[TID:{thread}] '
               '<level>[{level}]</level> '
               '[{file.path}:{function}:{line}] '
               '- '
               '<yellow>[RID:{extra[request_id]}]</yellow> '
               '<magenta>[{extra[type]}]</magenta> '
               '<WHITE>{message}</WHITE>')

SHORT_FORMAT = ('<green>[{time:HH:mm:ss.SSS}]</green> '
                '<level>[{level}]</level> '
                '<yellow>[RID:{extra[request_id]}]</yellow> '
                '<magenta>[{extra[type]}]</magenta> '
                '{message}')


def patch_request_id(record):
    record['extra'].update(request_id=RequestCtx.get_request_id())


logger.remove()

logger.add(sink=log_conf.file,
           format=FULL_FORMAT,
           level=log_conf.level,
           serialize=True,
           enqueue=True)

logger.add(sink=sys.stdout,
           format=SHORT_FORMAT if app_conf.debug else FULL_FORMAT,
           colorize=True,
           level=log_conf.level,
           enqueue=True)

_logger = logger.patch(patch_request_id).bind(project_name=app_conf.name)


runtime_log = _logger.bind(type=LoggerTypeEnum.RUNTIME.value)
request_start_log = _logger.bind(type=LoggerTypeEnum.REQUEST_START.value)
request_finish_log = _logger.bind(type=LoggerTypeEnum.REQUEST_FINISH.value)
exception_log = _logger.bind(type=LoggerTypeEnum.EXCEPTION.value)
lifespan_log = _logger.bind(type=LoggerTypeEnum.LIFESPAN.value)
pg_log = _logger.bind(type=LoggerTypeEnum.POSTGRES.value)
redis_log = _logger.bind(type=LoggerTypeEnum.REDIS.value)
middleware_log = _logger.bind(type=LoggerTypeEnum.MIDDLEWARE.value)
transaction_log = _logger.bind(type=LoggerTypeEnum.TRANSACTION.value)
