from app.apiserver.exception import AppException
from sqlalchemy import select, delete

from ._base import BaseRepo
from ._tables import UserInfo
from app.schema.base import PullDataFormat


class UserInfoRepo(BaseRepo):

    def __init__(self):
        self.t: UserInfo = UserInfo.instance()

    def select(self, user_id):
        stmt = select(self.t).filter(self.t.id != user_id)
        return self.execute(stmt)

    def list(self, page: int, limit: int, order_by: str, order_type, search=None):
        stmt = (select(*self.t.info_columns(),
                       self.t.total_count)
                .filter(self.t.name.like(f'%{search}%') if search else self.always_true())
                .order_by(self.order_expr(order_by, order_type)))

        df = self.execute(stmt.limit(limit).offset((page - 1) * limit))
        return self.split_total_column(df)

    def detail(self, user_id: int):
        stmt = (select(self.t.user_id,
                       self.t.name,
                       self.t.age,
                       self.t.gender)
                .where(self.t.id == user_id))
        data = self.execute(stmt, output=PullDataFormat.RECORDS)
        if len(data) == 0:
            raise AppException.UserNotExist(detail=f'user_id {user_id} not exist')
        else:
            return data[0]

    def delete(self, user_id: int):
        stmt = delete(self.t).where(self.t.id == user_id)
        self.execute(stmt)
