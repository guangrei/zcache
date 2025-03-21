# -*-coding:utf8;-*-
from zcache.Sync import Cache as SyncCache
from zcache.Async import Cache as AsyncCache
from typing import Union, Generator, Any, Type, Awaitable


class Cache:
    _init_future: Awaitable[AsyncCache]

    def __new__(  # type: ignore[misc]
        cls: Type["Cache"], *args: Any, Async: bool = False, **kwargs: Any
    ) -> Union[SyncCache, "Cache"]:
        if Async:
            instance = super().__new__(cls)
            instance._init_future = AsyncCache(*args, **kwargs)
            return instance
        else:
            ret: SyncCache = SyncCache(*args, **kwargs)
            return ret

    async def _init(self) -> AsyncCache:
        ret = await self._init_future
        return ret

    def __await__(self) -> Generator[Any, None, AsyncCache]:
        return self._init().__await__()


__version__ = "4.0.0"
__author__ = "Guangrei <myawn@pm.me>"
__license__ = "MIT"
