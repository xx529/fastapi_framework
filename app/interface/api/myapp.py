import httpx

from app.apiserver import slog
from app.apiserver.exception import AppException
from app.config import MyAppApiConf


class UserInfoQuery:

    @classmethod
    async def query_user(cls, user_id: int):

        async with httpx.AsyncClient() as client:
            response = await client.get(url=MyAppApiConf.url(endpoint='/user'),
                                        params={'user_id': user_id})
            if response.status_code == 500:
                slog.error(response.text)
                raise AppException.RemoteCallError()
            else:
                return response
