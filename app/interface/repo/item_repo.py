from sqlalchemy import Column, String

from app.apiserver.database import SingletonTable


class ItemInfo(SingletonTable):
    __tablename__ = 'item_info'

    name = Column(String(255), nullable=False, comment='商品名称')
    category = Column(String(255), nullable=False, comment='商品类目')
