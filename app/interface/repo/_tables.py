from contextlib import contextmanager
from typing import Dict

from sqlalchemy import BIGINT, Boolean, Column, DateTime, Float, func, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect

from app.apiserver import service_logger
from app.apiserver import slog
from app.config import PgDataBaseConf

Base = declarative_base()
engine = create_engine(url=PgDataBaseConf.jdbcurl, connect_args={}, pool_pre_ping=True, pool_recycle=1200)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_all_tables():
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
        """

        :rtype: object
        """
        with get_db() as db:
            return function(self, db, *args, **kwargs)

    return wrapper



table_class_instance: Dict[str, Base] = {}


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
            service_logger.info(f'create table: {cls.__tablename__}')
            cls.__table__.create(bind=cls._engine)
        else:
            service_logger.info(f'exist table: {cls.__tablename__}')

    @classmethod
    def is_exists(cls):
        return inspect(cls._engine).has_table(cls.__tablename__, schema=PgDataBaseConf.schema)


class ItemInfo(BaseTable):
    __tablename__ = 'item_info'

    name = Column(String(255), nullable=False, comment='商品名称')
    category = Column(String(255), nullable=False, comment='商品类目')


class OrderInfo(BaseTable):
    __tablename__ = 'order_info'

    user_id = Column(Integer, nullable=False, comment='购买者ID')
    item_id = Column(Integer, nullable=False, comment='商品ID')
    status = Column(Integer, nullable=False, comment='订单状态')
    amount = Column(Float, nullable=False, comment='订单金额')
    order_time = Column(TIMESTAMP, nullable=False, comment='订单时间')


class TaskRecord(BaseTable):
    __abstract__ = True
    __tablename__ = 'task_record_{task_id}'

    task_name = Column(String(255), nullable=False, comment='任务名称')
    task_type = Column(String(255), nullable=False, comment='任务类型')
    task_status = Column(Integer, nullable=False, comment='任务状态')


class UserInfo(BaseTable):
    __tablename__ = 'user_info'

    name = Column(String(255), nullable=False, comment='用户名')
    age = Column(Integer, nullable=False, comment='年龄')
    gender = Column(String(1), nullable=False, comment='性别')


class TaskRecordRepo:

    def __init__(self, task_id):
        self.table: TaskRecord = TaskRecord.instance(task_id=task_id)

    def create_tabel(self):
        self.table.create()

    @db_session
    def select(self, db, task_id):
        import pandas as pd
        print(task_id)
        print(pd.DataFrame(db.query(self.table.task_status,
                                    self.table.task_type)))


create_all_tables()


t = TaskRecordRepo(task_id=11)

t.select(task_id=1)


