import logging
import sys

from loguru import logger

from app.apiserver.context import RequestCtx
from app.config import config
from app.schema.enum import LoggerNameEnum


class InterceptHandler(logging.Handler):
    def emit(self, record):
        (logger
         .opt(depth=6, exception=record.exc_info)
         .bind(name=record.name,
               custom_name=record.name,
               project_name=config.app_conf.name,
               trace_id=RequestCtx.get_trace_id(),
               logging_extra=record.__dict__.get(config.log_conf.extra_key, None))
         .log(record.levelname, record.getMessage()))


logger_name_list = config.log_conf.catch

if config.pg_connection.debug is True:
    logger_name_list.append('sqlalchemy')

for logger_name in logger_name_list:
    log_obj = logging.getLogger(logger_name)
    log_obj.setLevel(logging.DEBUG)
    log_obj.handlers = [InterceptHandler()]

FULL_FORMAT = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> '
               f'<red>{config.app_conf.name}</red> '
               '[PID:{process}] '
               '[TID:{thread}] '
               '<level>[{level}]</level> '
               '[{file.path}:{function}:{line}] '
               '- '
               '<yellow>[RID:{extra[trace_id]}]</yellow> '
               '<magenta>[{name}]</magenta> '
               '<WHITE>{message}</WHITE>')

SHORT_FORMAT = ('<green>[{time:HH:mm:ss.SSS}]</green> '
                '<level>[{level}]</level> '
                '<yellow>[TraceID:{extra[trace_id]}]</yel'
                'low> '
                '<magenta>[{name}]</magenta> '
                '{message}')

logger.remove()

logger.add(sink=config.log_conf.file,
           format=FULL_FORMAT,
           level=config.log_conf.level,
           serialize=True,
           enqueue=True)

logger.add(sink=sys.stdout,
           format=SHORT_FORMAT if config.app_conf.debug else FULL_FORMAT,
           colorize=True,
           level=config.log_conf.level,
           enqueue=True)

_logger = logger

runtime_log = _logger.bind(custom_name=LoggerNameEnum.RUNTIME.value)
request_start_log = _logger.bind(custom_name=LoggerNameEnum.REQUEST_START.value)
request_finish_log = _logger.bind(custom_name=LoggerNameEnum.REQUEST_FINISH.value)
exception_log = _logger.bind(custom_name=LoggerNameEnum.EXCEPTION.value)
lifespan_log = _logger.bind(custom_name=LoggerNameEnum.LIFESPAN.value)
sql_log = _logger.bind(custom_name=LoggerNameEnum.SQL.value)
redis_log = _logger.bind(custom_name=LoggerNameEnum.REDIS.value)
middleware_log = _logger.bind(custom_name=LoggerNameEnum.MIDDLEWARE.value)
transaction_log = _logger.bind(custom_name=LoggerNameEnum.TRANSACTION.value)
kafka_log = _logger.bind(custom_name=LoggerNameEnum.KAFKA.value)
