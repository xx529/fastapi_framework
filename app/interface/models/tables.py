import warnings

from sqlalchemy import Column, Float, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr

from app.interface.models.base import BaseTable

warnings.filterwarnings('ignore')


class UserInfo(BaseTable):
    __tablename__ = 'user_info'
    __abstract__ = False

    name = Column(String(255), nullable=False, comment='用户名')
    age = Column(Integer, nullable=False, comment='年龄')
    gender = Column(String(1), nullable=False, comment='性别')

    @declared_attr
    def sex(self):
        return self.gender.label('sex')

    @declared_attr
    def user_id(self):
        return self.id.label('user_id')

    @classmethod
    def info_columns(cls):
        return [cls.user_id, cls.name, cls.age, cls.gender]


class ItemInfo(BaseTable):
    __tablename__ = 'item_info'
    __abstract__ = False

    name = Column(String(255), nullable=False, comment='商品名称')
    category = Column(String(255), nullable=False, comment='商品类目')


class OrderInfo(BaseTable):
    __tablename__ = 'order_info'
    __abstract__ = False

    user_id = Column(Integer, nullable=False, comment='购买者ID')
    item_id = Column(Integer, nullable=False, comment='商品ID')
    status = Column(Integer, nullable=False, comment='订单状态')
    amount = Column(Float, nullable=False, comment='订单金额')
    order_time = Column(TIMESTAMP, nullable=False, comment='订单时间')


class TaskRecord(BaseTable):
    __tablename__ = 'task_record_{task_id}'
    __abstract__ = True

    name = Column(String(255), nullable=False, comment='任务名称')
    category = Column(String(255), nullable=False, comment='任务类型')
    status = Column(Integer, nullable=False, comment='任务状态')


class TaskInfo(BaseTable):
    __tablename__ = 'task_info'
    __abstract__ = False

    name = Column(String(255), nullable=False, comment='任务名称')
    category = Column(String(255), nullable=False, comment='任务类型')
    status = Column(String(255), nullable=False, comment='任务状态')
    user_id = Column(Integer, nullable=False, comment='用户ID')
