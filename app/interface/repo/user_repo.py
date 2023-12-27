from sqlalchemy import select, text

from ._base import BaseRepo
from ._tables import UserInfo


class UserInfoRepo(BaseRepo):

    def __init__(self):
        self.t: UserInfo = UserInfo.instance()

    def select(self, user_id):
        stmt = select(self.t).filter(self.t.id != user_id)
        return self.execute(stmt)

    def list(self, page: int, limit: int, order_by: str, order_type, search=None):
        stmt = (select(*self.t.info_columns())
                .filter(self.t.name.like(f'%{search}%') if search else text('1=1'))
                .order_by(order_by))

        return self.execute(stmt.limit(limit).offset((page - 1) * limit))
