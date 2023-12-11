from sqlalchemy import Column, Float, Integer, TIMESTAMP

from app.apiserver.database import db_session, SingletonTable


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
