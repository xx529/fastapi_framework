from sqlalchemy import delete, select, update, insert
from datetime import datetime

from app.apiserver.exception import AppException
from app.interface.cache.redis import redis_cache
from app.schema.enum import RedisKeyEnum
from ._base import BaseRepo
from ._tables import UserInfo

user_detail_key = lambda user_id: f'{RedisKeyEnum.USER_REPO.value}:{user_id}-detail'
user_list_key = lambda page, limit, order_type, order_by: f'{RedisKeyEnum.USER_REPO.value}:{page}-{limit}-{order_by}-{order_type}-list'
user_list_condition = lambda page, limit, search: page == 1 and limit == 10 and search is None
del_user_list_key = lambda: f'{RedisKeyEnum.USER_REPO.value}:*-list'


class UserInfoRepo(BaseRepo):

    def __init__(self):
        self.t: UserInfo = UserInfo.instance()

    def create(self, name: str, age: int, gender: str):
        stmt = (insert(self.t)
                .values(name=name,
                        age=age,
                        gender=gender,
                        del_flag=False)
                .returning(self.t.user_id))
        return self.execute(stmt)['user_id'][0]

    @redis_cache.cache(key=user_list_key, condition=user_list_condition)
    def list(self, page: int, limit: int, order_by: str, order_type, search=None):
        stmt = (select(*self.t.info_columns(),
                       self.t.total_count())
                .filter(self.t.name.like(f'%{search}%') if search else self.always_true())
                .order_by(self.order_expr(order_by, order_type)))

        df = self.execute(stmt.limit(limit).offset((page - 1) * limit))
        return self.split_total_column(df)

    @redis_cache.cache(key=user_detail_key)
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

    @redis_cache.clear(key=del_user_list_key)
    def delete(self, user_id: int):
        stmt = delete(self.t).where(self.t.id == user_id)
        self.execute(stmt, output=None)

    @redis_cache.clear(key=user_detail_key)
    def update(self, user_id: int, name: str = None, city: str = None, age: int = None):
        # TODO 按需更新
        stmt = (update(self.t)
                .where(self.t.id == user_id)
                .values(name=name, city=city, age=age))
        self.execute(stmt, output=None)
