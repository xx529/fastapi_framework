from enum import Enum
from typing import Any

import redis as sync_redis
import redis.asyncio as async_redis

from app.config import redis_connection


class RedisKeyPrefix(str, Enum):
    base = 'base'


class Redis:
    _async_pool: async_redis.ConnectionPool = None
    _sync_pool: sync_redis.ConnectionPool = None
    expire_seconds = redis_connection.expire_seconds
    project_prefix = redis_connection.project_prefix

    def __init__(self, key_prefix: RedisKeyPrefix):
        self.key_prefix = key_prefix
        self.sync_redis = sync_redis.Redis(connection_pool=self._sync_pool)
        self.async_redis = async_redis.Redis(connection_pool=self._async_pool)

    def set(self, key: str, value: Any, expire_seconds=None):
        ex = expire_seconds or self.expire_seconds
        name = self._get_unique_key(key)
        self.sync_redis.set(name=name, value=value, ex=ex)

    def get(self, key: str) -> Any:
        name = self._get_unique_key(key)
        return self.sync_redis.get(name=name)

    def delete(self, key: str):
        name = self._get_unique_key(key)
        self.sync_redis.delete(name)

    async def async_set(self, key: str, value: Any, expire_seconds=None):
        ex = expire_seconds or self.expire_seconds
        name = self._get_unique_key(key)
        await self.async_redis.set(name=name, value=value, ex=ex)

    async def async_get(self, key: str) -> Any:
        name = self._get_unique_key(key)
        return await self.async_redis.get(name=name)

    async def async_delete(self, key: str):
        name = self._get_unique_key(key)
        await self.async_redis.delete(name)

    def _get_unique_key(self, key: str):
        return f'{self.project_prefix}:{self.key_prefix.value}:{key}'

    @classmethod
    def startup(cls):
        if not cls._async_pool:
            cls._async_pool = async_redis.ConnectionPool(host=redis_connection.host,
                                                         port=redis_connection.port,
                                                         db=redis_connection.db,
                                                         password=redis_connection.password,
                                                         decode_responses=True,
                                                         max_connections=redis_connection.max_connections)
        if not cls._sync_pool:
            cls._sync_pool = sync_redis.ConnectionPool(host=redis_connection.host,
                                                       port=redis_connection.port,
                                                       db=redis_connection.db,
                                                       password=redis_connection.password,
                                                       decode_responses=True,
                                                       max_connections=redis_connection.max_connections)

    @classmethod
    def shutdown(cls):
        if cls._async_pool:
            cls._async_pool.disconnect()
            cls._async_pool = None
        if cls._sync_pool:
            cls._sync_pool.disconnect()
            cls._sync_pool = None
