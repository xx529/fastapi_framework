from typing import List, Tuple

from app.apiserver.exception import AppException
from app.interface import UserInfoRepo, AsyncDataBaseTransaction
from app.schema.user import UserID, UserInfo


class UserService:

    @staticmethod
    async def create_user(name: str, age: int, gender: str) -> UserID:
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

        if len(data) == 0:
            raise AppException.UserNotExist(detail=f'user_id {user_id} not exist')
        else:
            return UserInfo(**data)

    @staticmethod
    async def delete_user(user_id: int) -> None:
        async with AsyncDataBaseTransaction() as db:
            await UserInfoRepo(db).delete(user_id=user_id)

    @staticmethod
    async def update_user(user_id: int, name: str = None, age: int = None, gender: str = None) -> None:
        async with AsyncDataBaseTransaction() as db:
            await UserInfoRepo(db).update(user_id=user_id,
                                          name=name,
                                          gender=gender,
                                          age=age)
