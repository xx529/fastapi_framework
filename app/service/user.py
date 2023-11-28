import faker
import pandas as pd


class UserService:

    @staticmethod
    def list(page, limit):
        f = faker.Faker(locale='zh_CN')
        user_ls = pd.DataFrame(data=[(x, f.name()) for x in range(100)],
                               columns=['id', 'name'])
        offset = (page - 1) * limit
        data = user_ls[offset: offset + limit].to_dict(orient='records')
        return data

    @staticmethod
    def detail(user_id):
        data = dict(id=user_id, name='张三', city='北京', age=18)
        return data
