from typing import List, Tuple

from app.apiserver.exception import AppExceptionEnum
from app.interface import UserInfoRepo, DataBaseTransaction
from app.schema.schemas.user import UserInfo
from app.schema.common import UserID


class UserService:

    @staticmethod
    async def create_user(name: str, age: int, gender: str) -> UserID:
        async with DataBaseTransaction() as db:
            user_id = await UserInfoRepo(db).create(name=name, age=age, gender=gender)
        return user_id

    @staticmethod
    async def list(page, limit, order_by, order_type, search) -> Tuple[List[UserInfo], int]:
        async with DataBaseTransaction(commit=False) as db:
            df_list, total = await UserInfoRepo(db).list(page=page,
                                                         limit=limit,
                                                         order_by=order_by,
                                                         order_type=order_type,
                                                         search=search)
        return df_list.to_dict(orient='records'), total

    @staticmethod
    async def detail(user_id: int) -> UserInfo:
        async with DataBaseTransaction(commit=False) as db:
            data = await UserInfoRepo(db).detail(user_id=user_id)

        if len(data) == 0:
            raise AppExceptionEnum.UserNotExist(detail=f'user_id {user_id} not exist')
        else:
            return UserInfo(**data)

    @staticmethod
    async def delete_user(user_id: int) -> None:
        async with DataBaseTransaction() as db:
            await UserInfoRepo(db).delete(user_id=user_id)

    @staticmethod
    async def update_user(user_id: int, name: str = None, age: int = None, gender: str = None) -> None:
        async with DataBaseTransaction() as db:
            await UserInfoRepo(db).update(user_id=user_id,
                                          name=name,
                                          gender=gender,
                                          age=age)
