import faker
import pandas as pd
import random


class UserService:

    @staticmethod
    def list(page, limit):
        f = faker.Faker(locale='zh_CN')
        user_ls = pd.DataFrame(data=[(x, f.name()) for x in range(100)],
                               columns=['user_id', 'name'])
        offset = (page - 1) * limit
        data = user_ls[offset: offset + limit].to_dict(orient='records')
        return data

    @staticmethod
    def detail(user_id):
        data = dict(user_id=user_id, name='张三', city='北京', age=18)
        return data

    @staticmethod
    def create(name, city=None, age=None):
        return {'user_id': random.randint(0, 100)}

    @staticmethod
    def delete(user_id):
        return None
