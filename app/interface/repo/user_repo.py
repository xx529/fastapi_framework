from sqlalchemy import delete, select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

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

    def __init__(self, db: AsyncSession):
        self.model: UserInfo = UserInfo
        self.db = db

    async def create(self, name: str, age: int, gender: str):
        stmt = (insert(self.model)
                .values(name=name,
                        age=age,
                        gender=gender,
                        del_flag=False)
                .returning(self.model.user_id))
        data = await self.async_exec(stmt, output='raw')
        user_id = data.first()
        await redis_cache.adelete(user_detail_key(user_id))
        redis_cache.clear_batch(del_user_list_key())
        return user_id

    @redis_cache.cache(key=user_list_key, condition=user_list_condition)
    async def list(self, page: int, limit: int, order_by: str, order_type, search=None):
        stmt = (select(*self.model.info_columns(),
                       self.model.total_count())
                .filter(self.model.name.like(f'%{search}%') if search else self.always_true())
                .order_by(self.order_expr(order_by, order_type)))

        df = await self.async_exec(stmt.limit(limit).offset((page - 1) * limit))
        return self.split_total_column(df)

    @redis_cache.cache(key=user_detail_key)
    async def detail(self, user_id: int):
        stmt = (select(self.model.user_id,
                       self.model.name,
                       self.model.age,
                       self.model.gender)
                .where(self.model.user_id == user_id))
        data = await self.async_exec(stmt, output='list')
        if len(data) == 0:
            raise AppException.UserNotExist(detail=f'user_id {user_id} not exist')
        else:
            return data[0]

    @redis_cache.clear(key=del_user_list_key)
    def delete(self, user_id: int):
        stmt = delete(self.model).where(self.model.id == user_id)
        self.exec(stmt, output=None)

    @redis_cache.clear(key=user_detail_key)
    def update(self, user_id: int, name: str = None, gender: str = None, age: int = None):
        stmt = (update(self.model)
                .where(self.model.id == user_id)
                .values(name=name if name is not None else self.model.name,
                        gender=gender if gender is not None else self.model.gender,
                        age=age if age is not None else self.model.age,
                        update_by='admin'))
        self.exec(stmt, output=None)
