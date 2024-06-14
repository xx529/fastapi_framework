from app.config.schema import (
    ApiConfig, AppConfig, AppServerConfig, DirConfig, GeneralDataBaseConnection, KafkaConfig, LoggerConfig,
    RedisConnection, ResourceFileConfig, settings, SystemInfo,
)

__project_dir = DirConfig()

config = AppConfig(
    system_info=SystemInfo(),
    project_dir=__project_dir,
    resource_files=ResourceFileConfig(path=__project_dir.resource),
    app_conf=AppServerConfig(**settings.appserver),
    log_conf=LoggerConfig(name='log', level=settings.log.level, path=__project_dir.general_log,
                          is_json_format=settings.log.is_json_format, extra_key=settings.log.extra_key,
                          catch=settings.log.catch),
    pg_connection=GeneralDataBaseConnection(**settings.pg),
    redis_conf=RedisConnection(**settings.redis),
    myapp_service_api_conf=ApiConfig(**settings.external_api.myapp),
    kafka_conf=KafkaConfig(**settings.kafka)
)
