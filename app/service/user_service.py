from typing import List, Tuple

from app.interface import UserInfoRepo, AsyncDataBaseTransaction
from app.schema.user import UserId, UserInfo


class UserService:
    @staticmethod
    async def create_user(name: str, age: int, gender: str) -> UserId:
        async with AsyncDataBaseTransaction() as db:
            user_id = await UserInfoRepo(db).create(name=name, age=age, gender=gender)
        return user_id

    @staticmethod
    async def list(page, limit, order_by, order_type, search) -> Tuple[List[UserInfo], int]:
        async with AsyncDataBaseTransaction(commit=False) as db:
            df_list, total = await UserInfoRepo(db).list(page=page,
                                                         limit=limit,
                                                         order_by=order_by,
                                                         order_type=order_type,
                                                         search=search)
        return df_list.to_dict(orient='records'), total

    @staticmethod
    async def detail(user_id: int) -> UserInfo:
        async with AsyncDataBaseTransaction(commit=False) as db:
            data = await UserInfoRepo(db).detail(user_id=user_id)
        return UserInfo(**data)

    @staticmethod
    def delete_user(user_id: int) -> None:
        # TODO 完成删除用户的业务逻辑
        async with AsyncDataBaseTransaction() as db:
            UserInfoRepo(db).delete(user_id=user_id)

    @staticmethod
    def update_user(user_id: int, name: str = None, age: int = None, gender: str = None) -> None:
        # TODO 完成更新用户的业务逻辑
        async with AsyncDataBaseTransaction() as db:
            UserInfoRepo(db).update(user_id=user_id, name=name, gender=gender, age=age)
