import os
import platform
import sys
from pathlib import Path
from typing import Dict, Literal

from dynaconf import Dynaconf
from pydantic import BaseModel, Field

current_dir = Path(__file__).parent
project_dir = current_dir.parent.parent

files = ['default.yaml',
         '*.yaml'
         '*.env',
         project_dir / 'settings.yaml']

settings = Dynaconf(root_path=current_dir,
                    envvar_prefix='APP',
                    settings_files=files,
                    load_dotenv=True,
                    lowercase_read=True,
                    merge_enabled=True)


class DirConfig(BaseModel):
    root: Path = Field(project_dir, description='项目根目录')
    app: Path = Field(None, description='程序源码目录')
    data: Path = Field(None, description='持久化保存的数据目录')
    log: Path = Field(None, description='日志目录')
    general_log: Path = Field(default=None, description='通用日志目录')
    resource: Path = Field(None, description='资源文件目录')

    def model_post_init(self, __context):
        self.app = self.root / 'app'
        self.data = self.root / 'data'
        self.log = self.data / 'log'
        self.general_log = self.log / 'general'
        self.resource = self.app / 'resource'

    def check_create_ls(self):
        return [self.general_log]


class LoggerConfig(BaseModel):
    name: str = Field(description='日志名称')
    level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(description='日志级别')
    path: Path = Field(description='日志文件路径')
    file: Path = Field(default=None, description='日志文件')

    def model_post_init(self, __context):
        if self.file is None:
            self.file = self.path / f'{self.name}.log'


class GeneralDataBaseConnection(BaseModel):
    host: str = Field(description='地址')
    port: int = Field(description='端口')
    user: str = Field(description='用户名')
    password: str = Field(description='密码')
    database: str = Field(description='数据库')
    db_schema: str = Field(description='schema')
    jdbcurl: str = Field(None, description='jdbcurl')
    async_jdbcurl: str = Field(None, description='异步 jdbcurl')

    def model_post_init(self, __context):
        self.jdbcurl = f'postgresql://{self.host}:{self.port}/{self.database}?user={self.user}&password={self.password}'
        self.async_jdbcurl = f'postgresql+asyncpg://{self.host}:{self.port}/{self.database}?user={self.user}&password={self.password}'


class RedisConnection(BaseModel):
    host: str = Field(description='地址')
    port: int = Field(description='端口')
    db: int = Field(description='数据库')
    password: str = Field(description='密码')
    timeout: int = Field(description='超时时间')
    max_connections: int = Field(description='最大连接数')
    project_prefix: str = Field(description='项目前缀')
    expire_seconds: int = Field(description='默认过期时间')


class SystemInfo(BaseModel):
    python: str = Field(sys.version, description='python版本')
    operation: str = Field(sys.platform, description='操作系统')
    cpus: int = Field(os.cpu_count(), description='cpu核数')
    arch: str = Field(platform.machine(), description='cpu架构')


class AppServerConfig(BaseModel):
    name: str = Field(description='服务名称')
    version: str = Field(description='服务当前版本')
    host: str = Field(description='服务地址')
    port: int = Field(description='服务端口')
    prefix: str = Field(description='url前缀')
    debug: bool = Field(description='是否开启debug模式')


class ResourceFileConfig(BaseModel):
    path: Path = Field(description='资源文件目录路径')
    demo: Path = Field(None, description='demo.txt文件')

    def model_post_init(self, __context):
        if self.demo is None:
            self.demo = self.path / 'demo.txt'


class ApiConfig(BaseModel):
    protocol: str = Field(description='协议')
    host: str = Field(description='地址')
    port: int = Field(description='端口')
    prefix: str = Field(description='url前缀')

    def url(self, path):
        return f'{self.protocol}://{self.host}:{self.port}{self.prefix}{path}'


class TopicConfig(BaseModel):
    enable: bool = Field(description='是否该 topic 启用')
    topic_name: str = Field(description='topic名称')
    group_id: str | None = Field(None, description='group id')
    num_consumers: int = Field(description='消费者数量')


class KafkaConfig(BaseModel):
    bootstrap_servers: str = Field(description='kafka地址')
    enable: bool = Field(description='是否启用')
    topics: Dict[str, TopicConfig] = Field(description='topic配置')
