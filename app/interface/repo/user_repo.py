from sqlalchemy import select
from ._tables import UserInfo
from ._base import BaseRepo


class UserInfoRepo(BaseRepo):

    def __init__(self):
        self.t: UserInfo = UserInfo.instance()

    def select_by_id(self, user_id):
        stmt = select(self.t).where(self.t.id == user_id)
        return self.pull(stmt)
