import sys

from loguru import logger

from app.config import lifespan_log_conf, request_log_conf, service_log_conf
from .ctx import request_id

logger.remove()

logger.add(sink=lifespan_log_conf.file,
           level=lifespan_log_conf.level,
           format=lifespan_log_conf.format,
           filter=lambda record: record['extra']['name'] == lifespan_log_conf.name)

logger.add(sink=sys.stdout,
           level=lifespan_log_conf.level,
           format=lifespan_log_conf.format,
           filter=lambda record: record['extra']['name'] == lifespan_log_conf.name)

logger.add(sink=request_log_conf.file,
           level=request_log_conf.level,
           format=request_log_conf.format,
           filter=lambda record: record['extra']['name'] == request_log_conf.name)

logger.add(sink=sys.stdout,
           level=request_log_conf.level,
           format=request_log_conf.format,
           filter=lambda record: record['extra']['name'] == request_log_conf.name)

logger.add(sink=service_log_conf.file,
           level=service_log_conf.level,
           format=service_log_conf.format,
           filter=lambda record: record['extra']['name'] == service_log_conf.name)

logger.add(sink=sys.stdout,
           level=service_log_conf.level,
           format=service_log_conf.format,
           filter=lambda record: record['extra']['name'] == service_log_conf.name)

lifespan_logger = logger.bind(name=lifespan_log_conf.name)
service_logger = logger.bind(name=service_log_conf.name)
request_logger = logger.bind(name=request_log_conf.name)


class Logger:

    @staticmethod
    def info(msg):
        request_logger.info(f'{request_id.get()} | {msg}')

    @staticmethod
    def debug(msg):
        request_logger.debug(f'{request_id.get()} | {msg}')

    @staticmethod
    def warning(msg):
        request_logger.warning(f'{request_id.get()} | {msg}')

    @staticmethod
    def error(msg):
        request_logger.error(f'{request_id.get()} | {msg}')
