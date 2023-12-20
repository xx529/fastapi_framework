from sqlalchemy import Column, Float, Integer, String, TIMESTAMP

from app.interface.repo._base import BaseTable, db_session


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
        self.t: TaskRecord = TaskRecord.instance(task_id=task_id)

    def create_tabel(self):
        self.t.create()

    @db_session
    def select(self, db, task_id):

        result = (db.query(self.t.task_type,
                           self.t.task_status)
                  .filter(self.t.task_status == '333'))
        return result


t = TaskRecordRepo(task_id=11)

t.select(task_id=1)


print(t.t.is_exists())

