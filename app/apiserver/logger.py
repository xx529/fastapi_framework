import sys

from loguru import logger

from app.config import lifespan_log_conf, request_log_conf, service_log_conf

logger.remove()

logger.add(sink=lifespan_log_conf.file,
           format=lifespan_log_conf.format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == lifespan_log_conf.name)

logger.add(sink=sys.stdout,
           format=lifespan_log_conf.format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == lifespan_log_conf.name)

logger.add(sink=request_log_conf.file,
           format=request_log_conf.format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == request_log_conf.name)

logger.add(sink=sys.stdout,
           level='INFO',
           format=request_log_conf.format,
           filter=lambda record: record['extra']['name'] == request_log_conf.name)

logger.add(sink=service_log_conf.file,
           format=service_log_conf.format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == service_log_conf.name)

logger.add(sink=sys.stdout,
           level='INFO',
           format=service_log_conf.format,
           filter=lambda record: record['extra']['name'] == service_log_conf.name)

lifespan_logger = logger.bind(name=lifespan_log_conf.name)
service_logger = logger.bind(name=service_log_conf.name)
request_logger = logger.bind(name=request_log_conf.name)
