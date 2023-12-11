import sys

from loguru import logger

from app.config import LogConf

logger.remove()

logger.add(sink=LogConf.lifespan_file,
           format=LogConf.lifespan_format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == LogConf.lifespan_name)

logger.add(sink=sys.stdout,
           format=LogConf.lifespan_format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == LogConf.lifespan_name)

logger.add(sink=LogConf.request_file,
           format=LogConf.request_format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == LogConf.request_name)

logger.add(sink=sys.stdout,
           level='INFO',
           format=LogConf.request_format,
           filter=lambda record: record['extra']['name'] == LogConf.request_name)

logger.add(sink=LogConf.service_file,
           format=LogConf.service_format,
           level='INFO',
           filter=lambda record: record['extra']['name'] == LogConf.service_name)

logger.add(sink=sys.stdout,
           level='INFO',
           format=LogConf.service_format,
           filter=lambda record: record['extra']['name'] == LogConf.service_name)

lifespan_logger = logger.bind(name=LogConf.lifespan_name)
service_logger = logger.bind(name=LogConf.service_name)
request_logger = logger.bind(name=LogConf.request_name)
