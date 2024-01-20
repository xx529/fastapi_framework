import random
from typing import List, Tuple

from app.apiserver.logger import runtime_log
from app.interface import UserInfoRepo
from app.schema.user import UserId, UserInfo, UserInfoForList


class UserService:

    @staticmethod
    def list(page, limit, order_by, order_type, search) -> Tuple[List[UserInfoForList], int]:
        df_list, total = UserInfoRepo().list(page=page,
                                             limit=limit,
                                             order_by=order_by,
                                             order_type=order_type,
                                             search=search)
        return df_list.to_dict(orient='records'), total

    @staticmethod
    def detail(user_id: int) -> UserInfo:
        data = UserInfoRepo().detail(user_id=user_id)
        return UserInfo(**data)

    @staticmethod
    def create(name: str, age: int, gender: str) -> UserId:
        # TODO 新增用户接口
        return random.randint(0, 100)

    @staticmethod
    def delete(user_id: int) -> None:
        UserInfoRepo().delete(user_id=user_id)

    @staticmethod
    def update(user_id: int, name: str = None, city: str = None, age: int = None) -> None:
        if all(map(lambda x: x is None, [name, city, age])):
            runtime_log.info('no need to update!')
            return

        UserInfoRepo().update(user_id=user_id, name=name, city=city, age=age)
