from sqlalchemy import select, text

from ._base import BaseRepo
from ._tables import UserInfo


class UserInfoRepo(BaseRepo):

    def __init__(self):
        self.t: UserInfo = UserInfo.instance()

    def select_by_id(self, user_id, search=None):
        stmt = (select(self.t.name,
                       self.t.age,
                       self.t.gender)
                .filter(self.t.id != user_id,
                        self.t.name.like(f'%{search}%') if search else text('1=1')))
        return self.execute(stmt)
