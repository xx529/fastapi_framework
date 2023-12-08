from app.apiserver.database import BaseTable, db_session
from sqlalchemy import Column, String, Integer


class UserInfo(BaseTable):
    __tablename__ = 'user_info'

    name = Column(String(255), nullable=False, comment='用户名')
    age = Column(Integer, nullable=False, comment='年龄')
    gender = Column(String(1), nullable=False, comment='性别')


class UserInfoRepo:

    @staticmethod
    @db_session
    def get_user_info(db, user_id):
        print(id(db))
        print(user_id)
        print('----')
        print(db.query(UserInfo).filter(UserInfo.id == user_id).count())
