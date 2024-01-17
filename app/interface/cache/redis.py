import asyncio
import inspect
import pickle
import time
from functools import wraps
from typing import Any, Callable

import redis as sync_redis
import redis.asyncio as async_redis

from app.apiserver.logger import redis_log
from app.config.schema import RedisConnection


class Redis:

    def __init__(self, conf: RedisConnection):
        self.conf = conf
        self.aclient: async_redis.Redis = None
        self.client: sync_redis.Redis = None
        self.redis_async_pools: async_redis.BlockingConnectionPool = None
        self.redis_sync_pools: sync_redis.BlockingConnectionPool = None

    def __call__(self, key: Callable, ttl: int = None):

        def layer(func):

            if asyncio.iscoroutinefunction(func):

                @wraps(func)
                async def ainner(*args, **kwargs):

                    cache_key = self.get_cache_key(key, func, *args, **kwargs)
                    if self.exists(cache_key):
                        result = await self.aget(key=cache_key)
                    else:
                        result = await func(*args, **kwargs)
                        await self.aset(key=cache_key, data=result, expire_seconds=ttl)
                    return result

                return ainner

            else:

                @wraps(func)
                def inner(*args, **kwargs):
                    cache_key = self.get_cache_key(key, func, *args, **kwargs)
                    if self.exists(cache_key):
                        result = self.get(key=cache_key)
                    else:
                        result = func(*args, **kwargs)
                        self.set(key=cache_key, data=result, expire_seconds=ttl)
                    return result

                return inner

        return layer

    def get(self, key: str) -> Any:
        name = self.get_full_key(key)
        redis_log.debug(f'get key: {name}')
        return pickle.loads(self.client.get(name=name))

    def set(self, key: str, value: Any, expire_seconds=None) -> None:
        ex = expire_seconds or self.conf.expire_seconds
        name = self.get_full_key(key)
        redis_log.debug(f'set key: {name}')
        self.client.set(name=name, value=pickle.dumps(value), ex=ex)

    def delete(self, key: str) -> None:
        name = self.get_full_key(key)
        self.client.delete(name)

    async def aget(self, key: str) -> Any:
        name = self.get_full_key(key)
        redis_log.debug(f'get key: {name}')
        return await pickle.loads(self.aclient.get(name=name))

    async def aset(self, key: str, value: Any, expire_seconds=None) -> None:
        ex = expire_seconds or self.conf.expire_seconds
        name = self.get_full_key(key)
        redis_log.debug(f'set key: {name}')
        await self.aclient.set(name=name, value=pickle.dumps(value), ex=ex)

    async def adelete(self, key: str) -> None:
        name = self.get_full_key(key)
        await self.aclient.delete(name)

    def delete_keys(self, keys):
        pipeline = self.client.pipeline()
        for key in keys:
            pipeline.delete(key)
        pipeline.execute()

    def clear_all(self):

        match_key = f'{self.conf.project_prefix}:*'
        keys = []
        for key in self.client.scan_iter(match_key, count=100):
            keys.append(key)
            if len(keys) >= 100:
                self.delete_keys(keys)
                keys = []
                time.sleep(0.01)
        else:
            self.delete_keys(keys)

    def exists(self, key):
        return self.client.exists(key)

    def get_full_key(self, key: str):
        return f'{self.conf.project_prefix}:{key}'

    def get_cache_key(self, key, func, *args, **kwargs):

        # 转换成统一 kwargs 的参数形式
        param_dict = dict(kwargs)
        for v, k in zip(args, inspect.signature(func).parameters.values()):
            param_dict[str(k)] = v

        # 获取需要的 keys
        select_keys = [str(x) for x in inspect.signature(key).parameters.values()]

        # 调用 lambda 函数生成 cache key
        cache_key = key(**{k: param_dict[k] for k in select_keys})

        # 合并前缀
        cache_key = f'{self.conf.project_prefix}:{cache_key}'
        print(cache_key)
        return cache_key

    def startup(self):
        self.redis_async_pools = async_redis.BlockingConnectionPool(host=self.conf.host,
                                                                    port=self.conf.port,
                                                                    db=self.conf.db,
                                                                    password=self.conf.password,
                                                                    max_connections=self.conf.max_connections)
        self.aclient = async_redis.Redis(connection_pool=self.redis_async_pools)

        self.redis_sync_pools = sync_redis.BlockingConnectionPool(host=self.conf.host,
                                                                  port=self.conf.port,
                                                                  db=self.conf.db,
                                                                  password=self.conf.password,
                                                                  max_connections=self.conf.max_connections)
        self.client = sync_redis.Redis(connection_pool=self.redis_sync_pools)

    async def shutdown(self):
        if self.redis_async_pools:
            redis_log.info('close async redis connection pools')
            await self.redis_async_pools.disconnect()
            self.redis_async_pools = None

        if self.redis_sync_pools:
            redis_log.info('close sync redis connection pools')
            self.redis_sync_pools.disconnect()
            self.redis_sync_pools = None

# class RedisDecoratorCache:
#
#     def __init__(self,
#                  client,
#                  key_prefix: str,
#                  default_ttl: int):
#
#         self.client = client
#         self.key_prefix = key_prefix
#         self.default_ttl = default_ttl
#
#     def cache(self,
#               key: Callable,
#               ttl: int = None):
#
#         def layer(func):
#
#             if asyncio.iscoroutinefunction(func):
#
#                 @wraps(func)
#                 async def ainner(*args, **kwargs):
#
#                     cache_key = self._get_cache_key(key, func, *args, **kwargs)
#                     if self._exists(cache_key):
#                         result = self._get(key=cache_key)
#                     else:
#                         result = await func(*args, **kwargs)
#                         self._set(key=cache_key, data=result, ttl=ttl)
#                     return result
#
#                 return ainner
#
#             else:
#
#                 @wraps(func)
#                 def inner(*args, **kwargs):
#                     cache_key = self._get_cache_key(key, func, *args, **kwargs)
#                     if self._exists(cache_key):
#                         result = self._get(key=cache_key)
#                     else:
#                         result = func(*args, **kwargs)
#                         self._set(key=cache_key, data=result, ttl=ttl)
#                     return result
#
#                 return inner
#
#         return layer
#
#     def clear_all(self):
#
#         match = '{}*'.format(self.key_prefix)
#         keys = []
#         for key in self.client.scan_iter(match, count=100):
#             keys.append(key)
#             if len(keys) >= 100:
#                 self._delete_keys(keys)
#                 keys = []
#                 time.sleep(0.01)
#         else:
#             self._delete_keys(keys)
#
#     def clear(self, key):
#         self._delete_keys([key])
#
#     def _set(self, key, data, ttl=None):
#         ttl = ttl or self.default_ttl
#         self.client.set(name=key, value=pickle.dumps(data), ex=ttl)
#
#     def _get(self, key):
#         return pickle.loads(self.client.get(key))
#
#     def _exists(self, key):
#         return self.client.exists(key)
#
#     def _delete_keys(self, keys):
#         pipeline = self.client.pipeline()
#         for key in keys:
#             pipeline.delete(key)
#         pipeline.execute()
#
#     def _get_cache_key(self, key, func, *args, **kwargs):
#
#         # 转换成统一 kwargs 的参数形式
#         param_dict = dict(kwargs)
#         for v, k in zip(args, inspect.signature(func).parameters.values()):
#             param_dict[str(k)] = v
#
#         # 获取需要的 keys
#         select_keys = [str(x) for x in inspect.signature(key).parameters.values()]
#
#         # 调用 lambda 函数生成 cache key
#         cache_key = key(**{k: param_dict[k] for k in select_keys})
#
#         # 合并前缀
#         cache_key = f'{self.key_prefix}:{cache_key}'
#         print(cache_key)
#         return cache_key
#
#
# cache = RedisDecoratorCache(client=_client,
#                             key_prefix='aigc:thinker:redis_decorator',
#                             default_ttl=10)

#
# @cache.cache(key=lambda a, aaa: f'{a}-{aaa}-test-1-cache')
# def fff(a, aaa, b):
#     print('inner')
#     df = pd.DataFrame(range(a))
#     return df
#
# for i in range(200):
#     fff(i, aaa='test', b='aaaaaaaaaaa')
#
#
# @cache.cache(key=lambda b: f'{b}-teeeeeee')
# async def fa(b):
#     print('ainner', fa.__name__)
#     await asyncio.sleep(0.1)
#     return b
#
#
# asyncio.run(fa('937840934u3'))
#
#
# # @redis_decorator.cache(keys=['b'])
# # def fb(b):
# #     print(fb.__name__, 'inner')
# #     return b
# #
# #
# class Test:
#
#     @cache.cache(key=lambda x: f'{x}-xxxxxxxxyeal!')
#     def fffff(self, x):
#         print('inner')
#         return x
#
# t1 = Test()
# print(t1.fffff(123))
#
# # print(fff(4))
# # print(fb(23))
# #
#
# #
# t2 = Test()
# print(t2.fffff(123))
# #
# # t3 = Test()
# # print(t3.fffff(123))
# #
#
# cache.clear('aigc:thinker:redis_decorator:195-test-test-1-cache')
#
# # def dec(name):
# #
# #     def layer(func):
# #
# #         def inner(*args, **kwargs):
# #             print(1)
# #             result = func(*args, **kwargs)
# #             print(2)
# #             print(name)
# #             return result
# #
# #         return inner
# #
# #     return layer
# #
# #
# # @dec(name='name')
# # def abc(a):
# #     return 1
# #
# #
# #
# # print(abc(13131231231231232131312313))
# #
# #
# #
# #
# #
# def dec(get_cache_key):
#     def layer(func):
#         @wraps(func)
#         def inner(*args, **kwargs):
#             param_dict = {}
#             for v, k in zip(args, inspect.signature(func).parameters.values()):
#                 param_dict[str(k)] = v
#
#             param_dict.update(kwargs)
#             print(param_dict)
#
#             select_keys = [str(x) for x in inspect.signature(get_cache_key).parameters.values()]
#             print(select_keys)
#
#             cache_keys = get_cache_key(**{k: param_dict[k] for k in select_keys})
#             print(cache_keys)
#
#             result = func(*args, **kwargs)
#
#             return result
#
#         return inner
#
#     return layer
