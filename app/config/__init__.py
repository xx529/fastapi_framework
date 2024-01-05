from app.config.schema import MyAppApiConf
from app.config.schema import (
    settings,
    DirConfig,
    LoggerConfig,
    ResourceFileConfig,
    SystemInfo,
    GeneralDataBaseConnection,
    RedisConnection,
    AppServerConfig,
)


system_info = SystemInfo()
project_dir = DirConfig()
resource_files = ResourceFileConfig(path=project_dir.resource)

app_conf = AppServerConfig(version=settings.appserver.version,
                           host=settings.appserver.host,
                           port=settings.appserver.port,
                           prefix='/api/v1')

request_log_conf = LoggerConfig(name='request',
                                format='{time:YYYY-MM-DD HH:mm:ss} | {thread.name} | {level} | {message}',
                                path=project_dir.request_log)

service_log_conf = LoggerConfig(name='service',
                                format='{time:YYYY-MM-DD HH:mm:ss} | {thread.name} | {level} | {message}',
                                path=project_dir.service_log)

lifespan_log_conf = LoggerConfig(name='lifespan',
                                 format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
                                 path=project_dir.lifespan_log)

pg_connection = GeneralDataBaseConnection(host=settings.pg.host,
                                          port=settings.pg.port,
                                          user=settings.pg.user,
                                          password=settings.pg.password,
                                          database=settings.pg.database,
                                          schema=settings.pg.schema)

redis_connection = RedisConnection(host=settings.redis.host,
                                   port=settings.redis.port,
                                   db=settings.redis.db,
                                   password=settings.redis.password,
                                   max_connections=settings.redis.max_connections,
                                   project_prefix=settings.redis.project_prefix,
                                   expire_seconds=settings.redis.expire_seconds)
