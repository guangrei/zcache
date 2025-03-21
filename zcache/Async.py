# -*-coding:utf8;-*-
from zcache.Storage.AsyncFileStorage import AsyncFileStorage
from zcache.Interface import (
    AsyncStorageInterface,
    AsyncPluginsInterface,
    AsyncDatabaseInterface,
)
import time
from typing import Any, Optional, Tuple, Dict, Generator
from typing_extensions import Self


class Cache(AsyncDatabaseInterface):
    def __init__(
        self,
        path: Optional[str] = None,
        limit: int = 0,
        storage: Optional[AsyncStorageInterface] = None,
        plugins: Optional[AsyncPluginsInterface] = None,
    ) -> None:
        self._init_future = self._init(path, limit, storage, plugins)

    async def _init(
        self,
        path: Optional[str] = None,
        limit: Optional[int] = 0,
        storage: Optional[AsyncStorageInterface] = None,
        plugins: Optional[AsyncPluginsInterface] = None,
    ) -> None:
        self.plugins = plugins
        self.__limit = limit
        if path is not None:
            path = path
        else:
            path = "zcache.json"
        if storage is not None:
            self._storage = storage
        else:
            s = await AsyncFileStorage(path)
            self._storage = s
        await self.__loadfile()

    async def _constructor(self) -> Self:
        await self._init_future
        return self

    def __await__(self) -> Generator[Any, None, Self]:
        return self._constructor().__await__()

    @property
    def databases(self) -> Dict[str, Any]:
        return self._databases

    @property
    def storage(self) -> AsyncStorageInterface:
        return self._storage

    async def __updatefile(self) -> None:
        await self._storage.save(self._databases)

    async def __loadfile(self) -> None:
        self._databases = await self._storage.load()
        self._databases["limit"] = self.__limit

    async def __exists(self, key: str) -> Tuple[bool, bool]:
        try:
            t = self._databases["data"][key]
            if t["ttl"] != 0:
                sisa = int(time.time()) - t["time"]
                if sisa >= t["ttl"]:
                    if self.plugins is not None:
                        await self.plugins.on_expired(self, key)
                    del self._databases["data"][key]
                    await self.__updatefile()
                    return False, False
                else:
                    return True, t["content"]
            else:
                return True, t["content"]
        except KeyError:
            return False, False

    async def __set(self, key: str, value: Any, ttl: Optional[int] = 0) -> None:
        if self.plugins is not None:
            value = await self.plugins.on_write(self, key, value)
        data: Dict[str, Any] = {}
        data["time"] = int(time.time())
        data["ttl"] = ttl
        data["content"] = value
        self._databases["data"][key] = data
        await self.__updatefile()

    async def has(self, key: str) -> bool:
        await self.__loadfile()
        r, v = await self.__exists(key)
        return r

    async def get(self, key: str, default: Any = None) -> Any:
        await self.__loadfile()
        r, v = await self.__exists(key)
        if r:
            if self.plugins is not None:
                ret = await self.plugins.on_read(self, key, v)
                return ret
            return v
        else:
            return default

    async def set(self, key: str, value: Any, ttl: int = 0) -> bool:
        # to optimize, __loadfile() not called here because already called in size()
        size = await self.size()
        if self._databases["limit"] != 0:
            if self._databases["limit"] == size:
                if self.plugins is not None:
                    await self.plugins.on_limit(self, key, value, ttl)
                return False
            else:
                await self.__set(key, value, ttl)
                return True
        else:
            await self.__set(key, value, ttl)
            return True

    async def delete(self, key: str) -> bool:
        # to optimize, __loadfile() not called here because already called in has()
        check = await self.has(key)
        if check:
            del self._databases["data"][key]
            await self.__updatefile()
            if self.plugins is not None:
                await self.plugins.on_delete(self, key)
            return True
        else:
            return False

    async def size(self) -> int:
        await self.__loadfile()
        ret = len(self._databases["data"])
        return ret

    async def reset(self) -> None:
        await self.__loadfile()
        self._databases["data"] = {}
        await self.__updatefile()
