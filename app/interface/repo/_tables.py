from sqlalchemy import BIGINT, Boolean, Column, DateTime, Float, func, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from app.config import PgDataBaseConf
from typing import Dict
from app.apiserver import slog

Base = declarative_base()


table_class_instance: Dict[str, Base] = {}


class BaseTable(Base):
    __abstract__ = True
    __allow_unmapped__ = True
    __table_args__ = {'schema': PgDataBaseConf.schema}
    engine = PgDataBaseConf.engine

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment="唯一ID值")
    create_at = Column(DateTime, default=func.now(), nullable=False, comment="创建时间")
    create_by = Column(String(64), index=False, nullable=False, comment="创建者")
    update_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="最后更新时间")
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
        self.db = None

    def create_tabel(self):
        self.table.create()



table = TaskRecordRepo(task_id=11)
table = TaskRecordRepo(task_id=11)
table = TaskRecordRepo(task_id=11)
table = TaskRecordRepo(task_id=11)