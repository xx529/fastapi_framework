from abc import ABC
from datetime import datetime
from typing import Dict

import pandas as pd
from sqlalchemy import asc, BIGINT, Boolean, Column, create_engine, DateTime, desc, func, inspect, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.apiserver.exception import AppException
from app.apiserver.logger import database_log
from app.config import pg_connection
from app.schema.enum import OrderTypeEnum, PullDataFormatEnum

Base = declarative_base()
engine = create_engine(url=pg_connection.jdbcurl, connect_args={}, pool_pre_ping=True, pool_recycle=1200)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# async_engine = create_async_engine(url=PgDataBaseConf.jdbcurl)
# AsyncSessionLocal = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=async_engine)

table_class_instance: Dict[str, Base] = {}


def create_all_pg_tables():
    Base.metadata.create_all(bind=engine)


class BaseTable(Base):
    __tablename__: str
    __abstract__ = True
    __allow_unmapped__ = True
    __table_args__ = {'schema': pg_connection.db_schema}
    _engine = engine

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment='唯一ID值')
    create_at = Column(DateTime, default=datetime.now(), nullable=False, comment='创建时间')
    create_by = Column(String(64), default='admin', index=False, nullable=False, comment='创建者')
    update_at = Column(DateTime, onupdate=datetime.now(), comment='最后更新时间')
    update_by = Column(String(64), index=False, comment='最后更新者')
    del_flag = Column(Boolean, index=False, default=False, nullable=False, comment='安全删除标记')

    @classmethod
    def instance(cls, **kwargs) -> Base:
        if getattr(cls, '__abstract__') is True:
            table_name = cls.__tablename__.format(**kwargs)
            if table_name not in table_class_instance:
                database_log.debug(f'create multi table class: {table_name}')
                table_class_instance[table_name] = type(table_name,
                                                        (cls,),
                                                        {'__tablename__': table_name})
            else:
                database_log.debug(f'get multi table class: {table_name}')
            return table_class_instance[table_name]
        else:
            return cls

    @classmethod
    def create(cls):
        if not cls.is_exists():
            database_log.debug(f'create table: {cls.__tablename__}')
            cls.__table__.create(bind=cls._engine)
        else:
            database_log.debug(f'exist table: {cls.__tablename__}')

    @classmethod
    def is_exists(cls):
        return inspect(cls._engine).has_table(cls.__tablename__, schema=pg_connection.schema)

    @classmethod
    def total_count(cls):
        return func.count(cls.id).over().label('total_count')


class ExecutorMixin(ABC):
    ...


class SqlExprMixin(ABC):
    @staticmethod
    def order_expr(order_by: str, order_type: OrderTypeEnum | None = None):
        match order_type:
            case OrderTypeEnum.ASC:
                return asc(order_by)
            case OrderTypeEnum.DESC:
                return desc(order_by)
            case _:
                return desc(order_by)

    @staticmethod
    def always_true():
        return text('1=1')

    @staticmethod
    def always_false():
        return text('1!=1')


class BaseRepo(ABC):

    @staticmethod
    def execute(stmt, output: PullDataFormatEnum = PullDataFormatEnum.PANDAS):
        db = SessionLocal()
        try:
            database_log.debug(str(stmt.compile(compile_kwargs={'literal_binds': True})).replace('\n', ''))
            result = db.execute(stmt)
            match output:
                case PullDataFormatEnum.RAW:
                    return result
                case PullDataFormatEnum.PANDAS:
                    return pd.DataFrame(result)
                case PullDataFormatEnum.RECORDS:
                    return pd.DataFrame(result).to_dict(orient='records')
        except Exception as e:
            database_log.error(f'execute error: {e}')
            db.rollback()
            raise AppException.DatabaseError(detail=str(e))
        finally:
            database_log.debug('close db session')
            db.close()

    @staticmethod
    async def async_execute(stmt, output: PullDataFormatEnum = PullDataFormatEnum.PANDAS):
        # TODO 异步查询数据库
        ...

    @staticmethod
    def split_total_column(df, col='total_count'):
        if len(df) == 0:
            total = 0
        else:
            total = df.pop(col).unique()[0]
        return df, total

    @staticmethod
    def order_expr(order_by: str, order_type: OrderTypeEnum | None = None):
        match order_type:
            case OrderTypeEnum.ASC:
                return asc(order_by)
            case OrderTypeEnum.DESC:
                return desc(order_by)
            case _:
                return desc(order_by)

    @staticmethod
    def always_true():
        return text('1=1')

    @staticmethod
    def always_false():
        return text('1!=1')
