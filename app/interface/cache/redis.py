from typing import Any

import redis as sync_redis
import redis.asyncio as async_redis

from app.config import local_redis
from app.config.schema import RedisConnection


class RedisConnectPool:
    _sync_pools = []
    _async_pools = []

    @classmethod
    def create_sync_pool(cls, conn: RedisConnection):
        pool = sync_redis.BlockingConnectionPool(host=conn.host,
                                                 port=conn.port,
                                                 db=conn.db,
                                                 timeout=conn.timeout,
                                                 password=conn.password,
                                                 max_connections=conn.max_connections)
        cls._sync_pools.append(pool)
        return pool

    @classmethod
    def startup(cls):
        ...

    @classmethod
    def shutdown(cls):
        ...

    @property
    def sync_pools(self):
        return self._sync_pools


class Redis:
    _sync_pool: sync_redis.ConnectionPool = None
    _async_pool: async_redis.ConnectionPool = None
    expire_seconds = local_redis.expire_seconds
    key_prefix = local_redis.project_prefix

    def __init__(self):
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

    def clear_all(self):
        ...

    def cache(self):
        ...

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
        return f'{self.key_prefix}:{key}'

    @classmethod
    def startup(cls):
        if not cls._async_pool:
            cls._async_pool = async_redis.ConnectionPool(host=local_redis.host,
                                                         port=local_redis.port,
                                                         db=local_redis.db,
                                                         password=local_redis.password,
                                                         max_connections=local_redis.max_connections)
        if not cls._sync_pool:
            cls._sync_pool = sync_redis.ConnectionPool(host=local_redis.host,
                                                       port=local_redis.port,
                                                       db=local_redis.db,
                                                       password=local_redis.password,
                                                       max_connections=local_redis.max_connections)

    @classmethod
    async def shutdown(cls):
        if cls._async_pool:
            await cls._async_pool.disconnect()
            cls._async_pool = None
        if cls._sync_pool:
            cls._sync_pool.disconnect()
            cls._sync_pool = None

# class RedisDecoratorCache:
#
#     def __init__(self,
#                  client: redis.Redis,
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
