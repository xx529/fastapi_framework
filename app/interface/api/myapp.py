import httpx
from loguru import logger

from app.apiserver.exception import AppExceptionEnum
from app.config import myapp_service_api_conf


class ExternalApi:
    ...


class UserInfoQuery(ExternalApi):

    @classmethod
    async def query_user(cls, user_id: int):

        async with httpx.AsyncClient() as client:
            response = await client.get(url=myapp_service_api_conf.url('/user'),
                                        params={'user_id': user_id})
            if response.status_code == 500:
                logger.error(response.text)
                raise AppExceptionEnum.RemoteCallError()
            else:
                return response
