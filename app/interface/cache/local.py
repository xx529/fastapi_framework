from abc import ABC


class BaseCache(ABC):

    def get(self, key, *args, **kwargs):
        raise NotImplementedError

    def set(self, key, value, *args, **kwargs):
        raise NotImplementedError

    def delete(self, key, *args, **kwargs):
        raise NotImplementedError

    def clear(self, *args, **kwargs):
        raise NotImplementedError

    async def async_get(self, key, *args, **kwargs):
        ...

    async def async_set(self, key, value, *args, **kwargs):
        ...


class DiskCache:
    ...


class MemCache:
    ...

    def get(self):
        ...

    def set(self):
        ...

    def clear(self):
        ...