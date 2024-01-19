from app.apiserver.exception import AppException
from sqlalchemy import select, delete

from ._base import BaseRepo
from ._tables import UserInfo
from ...schema.enum import PullDataFormatEnum
from app.interface.cache.redis import redis_cache
from app.schema.enum import RedisKeyEnum


class UserInfoRepo(BaseRepo):

    def __init__(self):
        self.t: UserInfo = UserInfo.instance()

    @redis_cache.cache(
        key=lambda page, limit, order_type, order_by: f'{RedisKeyEnum.USER_REPO.value}:{page}-{limit}-{order_by}-{order_type}-list',
        condition=lambda page, limit, search: page == 1 and limit == 10 and search is None
    )
    def list(self, page: int, limit: int, order_by: str, order_type, search=None):
        stmt = (select(*self.t.info_columns(),
                       self.t.total_count())
                .filter(self.t.name.like(f'%{search}%') if search else self.always_true())
                .order_by(self.order_expr(order_by, order_type)))

        df = self.execute(stmt.limit(limit).offset((page - 1) * limit))
        return self.split_total_column(df)

    @redis_cache.cache(key=lambda user_id: f'{RedisKeyEnum.USER_REPO.value}:{user_id}-detail')
    def detail(self, user_id: int):

        stmt = (select(self.t.user_id,
                       self.t.name,
                       self.t.age,
                       self.t.gender)
                .where(self.t.user_id == user_id))
        data = self.execute(stmt, output='list')
        if len(data) == 0:
            raise AppException.UserNotExist(detail=f'user_id {user_id} not exist')
        else:
            return data[0]

    @redis_cache.clear(key=lambda: f'{RedisKeyEnum.USER_REPO.value}:*-list')
    def delete(self, user_id: int):
        stmt = delete(self.t).where(self.t.id == user_id)
        self.execute(stmt, output=None)
