import httpx

from app.apiserver.exception import AppExceptionEnum
from app.config import api_conf


class UserInfoQuery:

    @classmethod
    async def query_user(cls, user_id: int):

        async with httpx.AsyncClient() as client:
            response = await client.get(url=api_conf.url(endpoint='/user'),
                                        params={'user_id': user_id})
            if response.status_code == 500:
                slog.error(response.text)
                raise AppExceptionEnum.RemoteCallError()
            else:
                return response
