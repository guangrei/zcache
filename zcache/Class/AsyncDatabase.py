# -*-coding:utf8;-*-
"""
The MIT License (MIT)

Copyright (c) 2022 zcache https://github.com/guangrei/zcache

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from zcache.Storage.AsyncFileStorage import AsyncFileStorage
from zcache.Interface import (
    AsyncStorageInterface,
    AsyncPluginsInterface,
    AsyncDatabaseInterface,
)
import time
from typing import Any, Optional, Tuple, Dict


class AsyncDatabase(AsyncDatabaseInterface):

    def __init__(
        self,
        path: Optional[str] = None,
        limit: int = 0,
        storage: Optional[AsyncStorageInterface] = None,
        plugins: Optional[AsyncPluginsInterface] = None,
    ) -> None:
        self._asyncargs = (path, limit, storage, plugins)

    async def init(self) -> None:
        await self._init(*self._asyncargs)

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
            s = AsyncFileStorage(path)
            await s.init()
            self._storage = s

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

    async def get(self, key: str) -> Any:
        await self.__loadfile()
        r, v = await self.__exists(key)
        if r:
            if self.plugins is not None:
                ret = await self.plugins.on_read(self, key, v)
                return ret
            return v
        else:
            return False

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
