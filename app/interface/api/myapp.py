import json

import httpx
from loguru import logger

from app.config import myapp_service_api_conf


class ExternalServiceAPI:
    BASE_URL: str

    @classmethod
    def request(cls, method: str, path: str, headers: dict = None, body: dict = None):
        endpoint = f'{method.upper()} {cls.BASE_URL}{path}'
        logger.info(f'request {endpoint} \n'
                    f'headers:\n'
                    f'{json.dumps(headers, indent=4) if headers else ""}'
                    f'\n'
                    f'body:\n'
                    f'{json.dumps(body, indent=4) if body else ""}')
        with httpx.Client() as client:
            response = client.request(method=method, url=f'{cls.BASE_URL}{path}', headers=headers, data=body)
            logger.info(f'response {endpoint} {response.status_code}')
            return response

    @classmethod
    async def async_request(cls, method: str, path: str, headers: dict = None, body: dict = None):
        endpoint = f'{method.upper()} {cls.BASE_URL}{path}'
        logger.info(f'request {endpoint} \n'
                    f'headers:\n'
                    f'{json.dumps(headers, indent=4) if headers else ""}'
                    f'\n'
                    f'body:\n'
                    f'{json.dumps(body, indent=4) if body else ""}')
        async with httpx.AsyncClient() as client:
            response = await client.request(method=method, url=f'{cls.BASE_URL}{path}', headers=headers, data=body)
            logger.info(f'response {endpoint} {response.status_code}')
            return response


class TestAPI(ExternalServiceAPI):
    BASE_URL = myapp_service_api_conf.url

    @classmethod
    async def test_api(cls):
        response = await cls.async_request(method='GET', path='/api/v1/system/test_get')
        return response
