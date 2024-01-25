from abc import ABC
from typing import Dict, Literal

import pandas as pd
from pydantic import BaseModel
from sqlalchemy import asc, BIGINT, Boolean, Column, create_engine, DateTime, desc, func, inspect, String, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.apiserver.exception import AppException
from app.apiserver.logger import pg_log
from app.config import pg_connection
from app.schema.enum import OrderTypeEnum

Base = declarative_base()

engine = create_engine(url=pg_connection.jdbcurl, connect_args={}, pool_pre_ping=True, pool_recycle=1200)
SessionLocal = sessionmaker(autoflush=True, autocommit=False, bind=engine)

sync_engine = create_async_engine(url=pg_connection.async_jdbcurl, future=True)
AsyncSessionLocal = sessionmaker(autoflush=True, autocommit=False, bind=sync_engine, class_=AsyncSession)

table_class_instance: Dict[str, Base] = {}


def create_all_pg_tables():
    Base.metadata.create_all(bind=engine)


def close_all_connection():
    SessionLocal.close_all()
    AsyncSessionLocal.close_all()


class BaseTable(Base):
    __tablename__: str
    __abstract__ = True
    __allow_unmapped__ = True
    __table_args__ = {'schema': pg_connection.db_schema}
    _engine = engine

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment='唯一ID值')
    create_at = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    create_by = Column(String(64), default='admin', index=False, nullable=False, comment='创建者')
    update_at = Column(DateTime, onupdate=func.now(), comment='最后更新时间')
    update_by = Column(String(64), index=False, comment='最后更新者')
    del_flag = Column(Boolean, index=False, default=False, nullable=False, comment='安全删除标记')

    @classmethod
    def instance(cls, **kwargs) -> Base:
        if getattr(cls, '__abstract__') is True:
            table_name = cls.__tablename__.format(**kwargs)
            if table_name not in table_class_instance:
                pg_log.debug(f'create multi table class: {table_name}')
                table_class_instance[table_name] = type(table_name,
                                                        (cls,),
                                                        {'__tablename__': table_name})
            else:
                pg_log.debug(f'get multi table class: {table_name}')
            return table_class_instance[table_name]
        else:
            return cls

    @classmethod
    def create(cls):
        if not cls.is_exists():
            pg_log.debug(f'create table: {cls.__tablename__}')
            cls.__table__.create(bind=cls._engine)
        else:
            pg_log.debug(f'exist table: {cls.__tablename__}')

    @classmethod
    def is_exists(cls):
        return inspect(cls._engine).has_table(cls.__tablename__, schema=pg_connection.schema)

    @classmethod
    def total_count(cls):
        return func.count(cls.id).over().label('total_count')


class ExecutorMixin(ABC):

    db: AsyncSession

    @staticmethod
    def exec(stmt, output: Literal['raw', 'pandas', 'list'] | BaseModel | None = 'pandas'):
        db = SessionLocal()
        pg_log.debug('sync db session')
        try:
            pg_log.debug(str(stmt.compile(compile_kwargs={'literal_binds': True})).replace('\n', ''))
            result = db.execute(stmt)
            db.commit()
            match output:
                case 'raw':
                    return result
                case 'pandas':
                    return pd.DataFrame(result)
                case 'list':
                    return pd.DataFrame(result).to_dict(orient='records')
                case BaseModel():
                    return output.model_validate(result)
                case None:
                    return None
        except Exception as e:
            pg_log.error(f'execute error: {e}')
            db.rollback()
            raise AppException.DatabaseError(detail=str(e))
        finally:
            pg_log.debug('close db session')
            db.close()

    async def async_exec(self, stmt, output: Literal['raw', 'pandas', 'list'] | BaseModel | None = 'pandas'):
        pg_log.debug(str(stmt.compile(compile_kwargs={'literal_binds': True})).replace('\n', ''))
        result = await self.db.execute(stmt)
        match output:
            case 'raw':
                return result.scalars()
            case 'pandas':
                return pd.DataFrame(result)
            case 'list':
                return pd.DataFrame(result).to_dict(orient='records')
            case BaseModel():
                return output.model_validate(result)
            case None:
                return None


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


class UtilsMixin(ABC):
    @staticmethod
    def split_total_column(df, col='total_count'):
        if len(df) == 0:
            total = 0
        else:
            total = df.pop(col).unique()[0]
        return df, total


class BaseRepo(ExecutorMixin, SqlExprMixin, UtilsMixin):
    ...

