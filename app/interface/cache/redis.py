import asyncio
import inspect
import pickle
import time
from functools import wraps
from typing import Any, Callable

import redis
import redis.asyncio as aredis

from app.apiserver.logger import redis_log
from app.config import redis_conf


class RedisCache:

    def __init__(self,
                 host: str = None,
                 port: int = None,
                 db: int = None,
                 password: str = None,
                 max_connections: int = None,
                 expire_seconds: int = 60,
                 key_prefix: str = 'redis',
                 client: redis.Redis = None,
                 aclient: aredis.Redis = None,
                 pools: redis.BlockingConnectionPool | redis.ConnectionPool = None,
                 apools: aredis.BlockingConnectionPool | aredis.ConnectionPool = None,

                 ):

        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.max_connections = max_connections
        self.expire_seconds = expire_seconds
        self.key_prefix = key_prefix
        self.aclient = aclient
        self.apools = apools
        self.client = client
        self.pools = pools

    def cache(self,
              key: Callable[..., str],
              condition: Callable[..., bool] = None,
              ttl: int = None):
        def layer(func):

            if asyncio.iscoroutinefunction(func):

                @wraps(func)
                async def ainner(*args, **kwargs):
                    if self.check_condition(condition, func, *args, **kwargs):
                        cache_key = self.exec_lambda_func(key, func, *args, **kwargs)
                        if self.exists(f'{self.key_prefix}:{cache_key}'):
                            result = await self.aget(key=cache_key)
                        else:
                            result = await func(*args, **kwargs)
                            await self.aset(key=cache_key, value=result, expire_seconds=ttl)
                    else:
                        result = await func(*args, **kwargs)
                    return result

                return ainner

            else:

                @wraps(func)
                def inner(*args, **kwargs):
                    if self.check_condition(condition, func, *args, **kwargs):
                        cache_key = self.exec_lambda_func(key, func, *args, **kwargs)
                        if self.exists(f'{self.key_prefix}:{cache_key}'):
                            result = self.get(key=cache_key)
                        else:
                            result = func(*args, **kwargs)
                            self.set(key=cache_key, value=result, expire_seconds=ttl)
                    else:
                        result = func(*args, **kwargs)
                    return result

                return inner

        return layer

    def clear(self, key: Callable[..., str]) -> None:

        def layer(func):

            if asyncio.iscoroutinefunction(func):

                @wraps(func)
                async def ainner(*args, **kwargs):
                    result = await func(*args, **kwargs)
                    clear_key = self.exec_lambda_func(key, func, *args, **kwargs)
                    redis_log.debug(f'clear key: {clear_key}')
                    self.clear_batch(match_key=f'{self.key_prefix}:{clear_key}')
                    return result

                return ainner

            else:
                @wraps(func)
                def inner(*args, **kwargs):
                    result = func(*args, **kwargs)
                    clear_key = self.exec_lambda_func(key, func, *args, **kwargs)
                    redis_log.debug(f'clear key: {clear_key}')
                    self.clear_batch(match_key=f'{self.key_prefix}:{clear_key}')
                    return result

                return inner

        return layer

    def get(self, key: str) -> Any:
        name = self.get_full_key(key)
        redis_log.debug(f'get key: {name}')
        if self.exists(key=name):
            return pickle.loads(self.client.get(name=name))
        else:
            return None

    def set(self, key: str, value: Any, expire_seconds=None) -> None:
        ex = expire_seconds or self.expire_seconds
        name = self.get_full_key(key)
        redis_log.debug(f'set key: {name}')
        self.client.set(name=name, value=pickle.dumps(value), ex=ex)

    def delete(self, key: str) -> None:
        name = self.get_full_key(key)
        redis_log.debug(f'del key: {name}')
        self.client.delete(name)

    async def aget(self, key: str) -> Any:
        name = self.get_full_key(key)
        redis_log.debug(f'get key: {name}')
        if self.exists(key=name):
            return pickle.loads(await self.aclient.get(name=name))
        else:
            return None

    async def aset(self, key: str, value: Any, expire_seconds=None) -> None:
        ex = expire_seconds or self.expire_seconds
        name = self.get_full_key(key)
        redis_log.debug(f'set key: {name}')
        await self.aclient.set(name=name, value=pickle.dumps(value), ex=ex)

    async def adelete(self, key: str) -> None:
        name = self.get_full_key(key)
        redis_log.debug(f'del key: {name}')
        await self.aclient.delete(name)

    def delete_keys(self, keys):
        pipeline = self.client.pipeline()
        for key in keys:
            pipeline.delete(key)
            redis_log.debug(f'del key: {key}')
        pipeline.execute()

    def clear_batch(self, match_key: str) -> None:

        keys = []
        batch_size = 100
        for key in self.client.scan_iter(match_key, count=batch_size):
            keys.append(key)
            if len(keys) >= batch_size:
                self.delete_keys(keys)
                keys.clear()
                time.sleep(0.01)
        else:
            self.delete_keys(keys)

    def clear_all_cache(self):
        self.clear_batch(match_key=f'{self.key_prefix}:*')

    def exists(self, key) -> bool:
        return self.client.exists(key)

    def get_full_key(self, key: str) -> str:
        return f'{self.key_prefix}:{key}'

    @staticmethod
    def exec_lambda_func(lambda_func: Callable, decorator_func: Callable, *args, **kwargs) -> str:

        # 转换成统一 kwargs 的参数形式
        param_dict = dict(kwargs)
        for v, k in zip(args, inspect.signature(decorator_func).parameters.values()):
            param_dict[str(k)] = v

        # 获取需要的 keys
        select_keys = [str(x) for x in inspect.signature(lambda_func).parameters.values()]

        # 调用 lambda 函数生成结果
        result = lambda_func(**{k: param_dict.get(k, None) for k in select_keys})

        return result

    def check_condition(self, lambda_func: Callable[..., bool], decorator_func: Callable, *args, **kwargs) -> bool:

        # 不需要检测时候
        if lambda_func is None:
            redis_log.debug(f'pass condition check')
            return True

        is_satisfied = self.exec_lambda_func(lambda_func, decorator_func, *args, **kwargs)
        if is_satisfied:
            redis_log.debug(f'cache condition is satisfied')
        else:
            redis_log.debug(f'cache condition is not satisfied')
        return is_satisfied

    def startup(self) -> "RedisCache":
        if not self.apools:
            self.apools = aredis.BlockingConnectionPool(host=self.host,
                                                        port=self.port,
                                                        db=self.db,
                                                        password=self.password,
                                                        max_connections=self.max_connections)
            self.aclient = aredis.Redis(connection_pool=self.apools)

        if not self.pools:
            self.pools = redis.BlockingConnectionPool(host=self.host,
                                                      port=self.port,
                                                      db=self.db,
                                                      password=self.password,
                                                      max_connections=self.max_connections)
            self.client = redis.Redis(connection_pool=self.pools)
        return self

    async def shutdown(self) -> None:
        if self.apools:
            await self.apools.disconnect()
            self.apools = None

        if self.pools:
            self.pools.disconnect()
            self.pools = None

    @classmethod
    def from_exist_pools(cls,
                         pool: redis.BlockingConnectionPool | redis.ConnectionPool,
                         apool: aredis.BlockingConnectionPool | aredis.ConnectionPool = None,
                         **kwargs
                         ) -> "RedisCache":
        return cls(client=redis.BlockingConnectionPool(connection_pool=pool),
                   aclient=aredis.BlockingConnectionPool(connection_poll=apool),
                   **kwargs)

    @classmethod
    def from_exist_client(cls,
                          client: redis.Redis,
                          aclient: aredis.Redis = None,
                          **kwargs
                          ) -> "RedisCache":
        return cls(client=client, aclient=aclient, **kwargs)

    @classmethod
    def create_instance(cls,
                        host: str = None,
                        port: int = None,
                        db: int = None,
                        password: str = None,
                        max_connections: int = None,
                        startup: bool = False,
                        **kwargs
                        ) -> "RedisCache":
        instance = cls(host=host, port=port, db=db, password=password, max_connections=max_connections, **kwargs)
        if startup:
            instance.startup()
        return instance


redis_cache = RedisCache(host=redis_conf.host,
                         port=redis_conf.port,
                         db=redis_conf.db,
                         password=redis_conf.password,
                         max_connections=redis_conf.max_connections)
