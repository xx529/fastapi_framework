import random

import faker
import pandas as pd

from app.interface import UserInfoRepo, TaskRecordRepo
from app.schema.user import UserId


class UserService:

    @staticmethod
    def list(page, limit, order_by, order_type, search):
        df_list = UserInfoRepo().list(
            page=page,
            limit=limit,
            order_by=order_by,
            order_type=order_type,
            search=search
        )
        return df_list.to_dict(orient='records')

    @staticmethod
    def detail(user_id):
        data = dict(user_id=user_id, name='张三', city='北京', age=18, gender='男')
        return data

    @staticmethod
    def create(name, city=None, age=None) -> UserId:
        return random.randint(0, 100)

    @staticmethod
    def delete(user_id):
        return None

    @staticmethod
    def update(user_id, name, city, age):
        return None
