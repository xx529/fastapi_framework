from abc import ABC
from contextlib import contextmanager
from typing import Dict

from sqlalchemy import BIGINT, Boolean, Column, create_engine, DateTime, func, inspect, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.apiserver.logger import service_logger as slog
from app.config import PgDataBaseConf

Base = declarative_base()
engine = create_engine(url=PgDataBaseConf.jdbcurl, connect_args={}, pool_pre_ping=True, pool_recycle=1200)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

table_class_instance: Dict[str, Base] = {}


def create_all_pg_tables():
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_session(function):
    def wrapper(self: object, *args: object, **kwargs: object) -> object:
        with get_db() as db:
            return function(self, db, *args, **kwargs)

    return wrapper


class BaseTable(Base):
    __tablename__: str
    __abstract__ = True
    __allow_unmapped__ = True
    __table_args__ = {'schema': PgDataBaseConf.schema}
    _engine = engine

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment="唯一ID值")
    create_at = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    create_by = Column(String(64), default=func.now(), index=False, nullable=False, comment="创建者")
    update_at = Column(DateTime, onupdate=func.now(), comment="最后更新时间")
    update_by = Column(String(64), index=False, comment="最后更新者")
    del_flag = Column(Boolean, index=False, default=False, nullable=False, comment="安全删除标记")

    @classmethod
    def instance(cls, **kwargs) -> Base:
        if getattr(cls, '__abstract__') is True:
            table_name = cls.__tablename__.format(**kwargs)
            if table_name not in table_class_instance:
                slog.info(f'create multi table class: {table_name}')
                table_class_instance[table_name] = type(table_name,
                                                        (cls,),
                                                        {'__tablename__': table_name})
            else:
                slog.info(f'get multi table class: {table_name}')
            return table_class_instance[table_name]
        else:
            return cls

    @classmethod
    def create(cls):
        if not cls.is_exists():
            slog.info(f'create table: {cls.__tablename__}')
            cls.__table__.create(bind=cls._engine)
        else:
            slog.info(f'exist table: {cls.__tablename__}')

    @classmethod
    def is_exists(cls):
        return inspect(cls._engine).has_table(cls.__tablename__, schema=PgDataBaseConf.schema)


class BaseRepo(ABC):

    def pull(self, stmt):
        print(2334234234)
        ...

    def execute(self):
        ...
