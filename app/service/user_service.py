import random

from app.interface import UserInfoRepo
from app.schema.user import UserId


class UserService:

    @staticmethod
    def list(page, limit, order_by, order_type, search):
        df_list, total = UserInfoRepo().list(page=page,
                                             limit=limit,
                                             order_by=order_by,
                                             order_type=order_type,
                                             search=search)
        return df_list.to_dict(orient='records'), total

    @staticmethod
    def detail(user_id):
        data = UserInfoRepo().detail(user_id=user_id)
        return data

    @staticmethod
    def create(name, age=None) -> UserId:
        return random.randint(0, 100)

    @staticmethod
    def delete(user_id):
        UserInfoRepo().delete(user_id=user_id)

    @staticmethod
    def update(user_id, name, city, age):
        return None
