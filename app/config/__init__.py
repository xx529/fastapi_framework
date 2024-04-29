from app.config.schema import (
    ApiConfig, AppConfig, AppServerConfig, DirConfig, GeneralDataBaseConnection, KafkaConfig, LoggerConfig,
    RedisConnection, ResourceFileConfig, settings, SystemInfo,
)

system_info = SystemInfo()
project_dir = DirConfig()
resource_files = ResourceFileConfig(path=project_dir.resource)
app_conf = AppServerConfig(**settings.appserver, prefix='/api/v1')
log_conf = LoggerConfig(name='log', level=settings.log.level, path=project_dir.general_log)
pg_connection = GeneralDataBaseConnection(**settings.pg)
redis_conf = RedisConnection(**settings.redis)
myapp_service_api_conf = ApiConfig(**settings.external_api.myapp)
kafka_conf = KafkaConfig(**settings.kafka)

config = AppConfig(
    system_info=SystemInfo(),
    project_dir=DirConfig(),
    resource_files=ResourceFileConfig(path=project_dir.resource),
    app_conf=AppServerConfig(**settings.appserver, prefix='/api/v1'),
    log_conf=LoggerConfig(name='log', level=settings.log.level, path=project_dir.general_log),
    pg_connection=GeneralDataBaseConnection(**settings.pg),
    redis_conf=RedisConnection(**settings.redis),
    myapp_service_api_conf=ApiConfig(**settings.external_api.myapp),
    kafka_conf=KafkaConfig(**settings.kafka)
)
