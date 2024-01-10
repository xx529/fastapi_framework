import os
import platform
import sys
from pathlib import Path
from typing import Literal

from dynaconf import Dynaconf
from pydantic import BaseModel, Field, model_validator

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
    request_log: Path = Field(None, description='请求日志目录')
    service_log: Path = Field(None, description='服务日志目录')
    lifespan_log: Path = Field(None, description='启停日志目录')
    resource: Path = Field(None, description='资源文件目录')

    @model_validator(mode='after')
    def set_values(self):
        self.app = self.root / 'app'
        self.data = self.root / 'data'
        self.log = self.data / 'log'
        self.request_log = self.log / 'request'
        self.service_log = self.log / 'service'
        self.lifespan_log = self.log / 'lifespan'
        self.resource = self.app / 'resource'

    def check_create_ls(self):
        return [self.request_log, self.service_log, self.lifespan_log]


class LoggerConfig(BaseModel):
    name: Literal['request', 'service', 'lifespan'] = Field(description='日志名称')
    level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(description='日志级别')
    format: str = Field(description='日志格式')
    path: Path = Field(description='日志文件路径')
    file: Path = Field(None, description='日志文件')

    @model_validator(mode='after')
    def set_values(self):
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

    @model_validator(mode='after')
    def set_values(self):
        self.jdbcurl = f'postgresql://{self.host}:{self.port}/{self.database}?user={self.user}&password={self.password}'


class RedisConnection(BaseModel):
    host: str = Field(description='地址')
    port: int = Field(description='端口')
    db: int = Field(description='数据库')
    password: str = Field(description='密码')
    max_connections: int = Field(description='最大连接数')
    project_prefix: str = Field(description='项目前缀')
    expire_seconds: int = Field(description='默认过期时间')


class SystemInfo(BaseModel):
    python: str = Field(sys.version, description='python版本')
    operation: str = Field(sys.platform, description='操作系统')
    cpus: int = Field(os.cpu_count(), description='cpu核数')
    arch: str = Field(platform.machine(), description='cpu架构')


class AppServerConfig(BaseModel):
    version: str = Field(description='服务当前版本')
    host: str = Field(description='服务地址')
    port: int = Field(description='服务端口')
    prefix: str = Field(description='url前缀')


class ResourceFileConfig(BaseModel):
    path: Path = Field(description='资源文件目录路径')
    demo: Path = Field(None, description='demo.txt文件')

    @model_validator(mode='after')
    def set_values(self):
        if self.demo is None:
            self.demo = self.path / 'demo.txt'


class ApiConfig(BaseModel):
    protocol: str = Field(description='协议')
    host: str = Field(description='地址')
    port: int = Field(description='端口')
    prefix: str = Field(description='url前缀')

    def url(self, path):
        return f'{self.protocol}://{self.host}:{self.port}{self.prefix}{path}'
