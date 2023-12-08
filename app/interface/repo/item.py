from app.apiserver.database import BaseTable
from sqlalchemy import Column, String


class ItemInfo(BaseTable):
    __tablename__ = 'item_info'

    name = Column(String(255), nullable=False, comment='商品名称')
    category = Column(String(255), nullable=False, comment='商品类目')
