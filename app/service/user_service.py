from typing import List, Tuple

from app.interface import UserInfoRepo
from app.schema.user import UserId, UserInfo


class UserService:
    @staticmethod
    def create_user(name: str, age: int, gender: str) -> UserId:
        user_id = UserInfoRepo().create(name=name, age=age, gender=gender)
        return user_id

    @staticmethod
    async def list(page, limit, order_by, order_type, search) -> Tuple[List[UserInfo], int]:
        df_list, total = await UserInfoRepo().list(page=page,
                                                   limit=limit,
                                                   order_by=order_by,
                                                   order_type=order_type,
                                                   search=search)
        return df_list.to_dict(orient='records'), total

    @staticmethod
    async def detail(user_id: int) -> UserInfo:
        data = await UserInfoRepo().detail(user_id=user_id)
        return UserInfo(**data)

    @staticmethod
    def delete_user(user_id: int) -> None:
        UserInfoRepo().delete(user_id=user_id)

    @staticmethod
    def update_user(user_id: int, name: str = None, age: int = None, gender: str = None) -> None:
        UserInfoRepo().update(user_id=user_id, name=name, gender=gender, age=age)
