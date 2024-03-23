import sys

from loguru import logger

from app.config import app_conf, log_conf
from app.schema.enum import LoggerTypeEnum

from loguru import logger
import logging

# logger.add(BASE_DIR/'run.log', serialize='json')


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


logger_name_list = [name for name in logging.root.manager.loggerDict]

for logger_name in logger_name_list:
    logging.getLogger(logger_name).setLevel(10)
    logging.getLogger(logger_name).handlers = []
    logging.getLogger(logger_name).addHandler(InterceptHandler())


FULL_FORMAT = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> '
               # '<red>{extra[project_name]}</red> '
               '[PID:{process}] '
               '[TID:{thread}] '
               '<level>[{level}]</level> '
               '[{file.path}:{function}:{line}] '
               '- '
               # '<yellow>[RID:{extra[trace_id]}]</yellow> '
               # '<magenta>[{extra[log_name]}]</magenta> '
               '<WHITE>{message}</WHITE>')

SHORT_FORMAT = ('<green>[{time:HH:mm:ss.SSS}]</green> '
                '<level>[{level}]</level> '
                # '<yellow>[TraceID:{extra[trace_id]}]</yellow> '
                # '<magenta>[{extra[log_name]}]</magenta> '
                '{message}')

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

_logger = logger.bind(project_name=app_conf.name)

runtime_log = _logger.bind(log_name=LoggerTypeEnum.RUNTIME.value)
request_start_log = _logger.bind(log_name=LoggerTypeEnum.REQUEST_START.value)
request_finish_log = _logger.bind(log_name=LoggerTypeEnum.REQUEST_FINISH.value)
exception_log = _logger.bind(log_name=LoggerTypeEnum.EXCEPTION.value)
lifespan_log = _logger.bind(log_name=LoggerTypeEnum.LIFESPAN.value)
pg_log = _logger.bind(log_name=LoggerTypeEnum.POSTGRES.value)
redis_log = _logger.bind(log_name=LoggerTypeEnum.REDIS.value)
middleware_log = _logger.bind(log_name=LoggerTypeEnum.MIDDLEWARE.value)
transaction_log = _logger.bind(log_name=LoggerTypeEnum.TRANSACTION.value)
