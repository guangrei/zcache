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
from zcache.Storage.BaseFileStorage import BaseFileStorage
from zcache.Interface import StorageInterface, PluginsInterface, DatabaseInterface
import time
from typing import Any, Optional, Tuple, Dict


class Database(DatabaseInterface):

    def __init__(
        self,
        path: Optional[str] = None,
        limit: int = 0,
        storage: Optional[StorageInterface] = None,
        plugins: Optional[PluginsInterface] = None,
    ) -> None:
        self.plugins = plugins or None
        if path is not None:
            path = path
        else:
            path = "zcache.json"
        self._storage = storage or BaseFileStorage(path)
        self.__limit = limit

    @property
    def databases(self) -> Dict[str, Any]:
        return self._databases

    @property
    def storage(self) -> StorageInterface:
        return self._storage

    def __updatefile(self) -> None:
        self._storage.save(self._databases)

    def __loadfile(self) -> None:
        self._databases = self._storage.load()
        self._databases["limit"] = self.__limit

    def __exists(self, key: str) -> Tuple[bool, bool]:
        try:
            t = self._databases["data"][key]
            if t["ttl"] != 0:
                sisa = int(time.time()) - t["time"]
                if sisa >= t["ttl"]:
                    if self.plugins is not None:
                        self.plugins.on_expired(self, key)
                    del self._databases["data"][key]
                    self.__updatefile()
                    return False, False
                else:
                    return True, t["content"]
            else:
                return True, t["content"]
        except KeyError:
            return False, False

    def __set(self, key: str, value: Any, ttl: Optional[int] = 0) -> None:
        if self.plugins is not None:
            value = self.plugins.on_write(self, key, value)
        data: Dict[str, Any] = {}
        data["time"] = int(time.time())
        data["ttl"] = ttl
        data["content"] = value
        self._databases["data"][key] = data
        self.__updatefile()

    def has(self, key: str) -> bool:

        self.__loadfile()
        r, v = self.__exists(key)
        return r

    def get(self, key: str) -> Any:

        self.__loadfile()
        r, v = self.__exists(key)
        if r:
            if self.plugins is not None:
                return self.plugins.on_read(self, key, v)
            return v
        else:
            return None

    def set(self, key: str, value: Any, ttl: int = 0) -> bool:

        # to optimize, __loadfile() not called here because already called in size()
        size = self.size()
        if self._databases["limit"] != 0:
            if self._databases["limit"] == size:
                if self.plugins is not None:
                    self.plugins.on_limit(self, key, value, ttl)
                return False
            else:
                self.__set(key, value, ttl)
                return True
        else:
            self.__set(key, value, ttl)
            return True

    def delete(self, key: str) -> bool:

        # to optimize, __loadfile() not called here because already called in has()
        check = self.has(key)
        if check:
            if self.plugins is not None:
                self.plugins.on_delete(self, key)
            del self._databases["data"][key]
            self.__updatefile()
            return True
        else:
            return False

    def size(self) -> int:
        self.__loadfile()
        ret = len(self._databases["data"])
        return ret

    def reset(self) -> None:
        self.__loadfile()
        self._databases["data"] = {}
        self.__updatefile()
