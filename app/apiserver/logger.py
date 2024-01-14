import sys

from loguru import logger

from app.config import lifespan_log_conf, runtime_log_conf, service_log_conf
from .context import RequestCtx

logger.remove()

logger.add(sink=lifespan_log_conf.file,
           level=lifespan_log_conf.level,
           format=lifespan_log_conf.format,
           filter=lambda record: record['extra']['name'] == lifespan_log_conf.name)

logger.add(sink=sys.stdout,
           level=lifespan_log_conf.level,
           format=lifespan_log_conf.format,
           filter=lambda record: record['extra']['name'] == lifespan_log_conf.name)

logger.add(sink=runtime_log_conf.file,
           level=runtime_log_conf.level,
           format=runtime_log_conf.format,
           filter=lambda record: record['extra']['name'] == runtime_log_conf.name)

logger.add(sink=sys.stdout,
           level=runtime_log_conf.level,
           format=runtime_log_conf.format,
           filter=lambda record: record['extra']['name'] == runtime_log_conf.name)

logger.add(sink=service_log_conf.file,
           level=service_log_conf.level,
           format=service_log_conf.format,
           filter=lambda record: record['extra']['name'] == service_log_conf.name)

logger.add(sink=sys.stdout,
           level=service_log_conf.level,
           format=service_log_conf.format,
           filter=lambda record: record['extra']['name'] == service_log_conf.name)

lifespan_logger = logger.bind(name=lifespan_log_conf.name)
_service_logger = logger.bind(name=service_log_conf.name)
_runtime_logger = logger.bind(name=runtime_log_conf.name)


class Logger:

    def __init__(self, logger_obj):
        self.log = logger_obj

    def info(self, msg):
        self.log.info(f'{RequestCtx.get_request_id()} | {msg}')

    def debug(self, msg):
        self.log.debug(f'{RequestCtx.get_request_id()} | {msg}')

    def warning(self, msg):
        self.log.warning(f'{RequestCtx.get_request_id()} | {msg}')

    def error(self, msg):
        self.log.error(f'{RequestCtx.get_request_id()} | {msg}')


runtime_logger = Logger(_runtime_logger)
service_logger = Logger(_service_logger)
