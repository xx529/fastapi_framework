import random

import faker
import pandas as pd

from app.interface import UserInfoRepo, TaskRecordRepo
from app.schema.user import UserId


class UserService:

    @staticmethod
    def list(page, limit, search):
        user_info = UserInfoRepo().select_by_id(user_id=1, search=search)
        task_info = TaskRecordRepo(task_id=11).select_by_id(row_id=5)

        f = faker.Faker(locale='zh_CN')
        user_ls = pd.DataFrame(data=[(x, f.name()) for x in range(100)],
                               columns=['user_id', 'name'])
        offset = (page - 1) * limit
        data = user_ls[offset: offset + limit].to_dict(orient='records')

        return data

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
