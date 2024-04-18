import httpx
from loguru import logger

from app.apiserver.exception import AppExceptionEnum
from app.config import myapp_service_api_conf


class ExternalServiceAPI:

    BASE_URL: str

    def request(self):
        ...

    @classmethod
    async def async_request(cls, method: str, path: str, headers: dict = None, body: dict = None):
        logger.info(f'request {method.upper()} {cls.BASE_URL}{path}')
        async with httpx.AsyncClient() as client:
            response = await client.request(method=method, url=f'{cls.BASE_URL}{path}', headers=headers,  data=body)
            return response


class UserInfoQuery(ExternalServiceAPI):

    BASE_URL = myapp_service_api_conf.url

    @classmethod
    async def query_user(cls):
        response = await cls.async_request(method='GET', path='/health/heartbeat')
        return response
