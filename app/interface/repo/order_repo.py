from app.apiserver.database import SingletonTable, db_session
from sqlalchemy import Column, Integer, Float, TIMESTAMP


class OrderInfo(SingletonTable):
    __tablename__ = 'order_info'

    user_id = Column(Integer, nullable=False, comment='购买者ID')
    item_id = Column(Integer, nullable=False, comment='商品ID')
    status = Column(Integer, nullable=False, comment='订单状态')
    amount = Column(Float, nullable=False, comment='订单金额')
    order_time = Column(TIMESTAMP, nullable=False, comment='订单时间')


class OrderInfoRepo:
    @staticmethod
    @db_session
    def get_order_info(db, order_id):
        print(id(db))
        print(order_id)