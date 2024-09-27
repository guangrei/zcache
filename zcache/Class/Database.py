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
from zcache.Interface.Storage import Storage as StorageInterface
from zcache.Interface.Plugins import Plugins as PluginsInterface
import time


class Database:

    def __init__(
        self,
        path=None,
        limit=0,
        storage=BaseFileStorage,
        plugins=None,
        StorageArgs=None,
    ):
        if plugins is not None and not issubclass(plugins, PluginsInterface):
            raise NotImplementedError
        self.plugins = plugins
        if not issubclass(storage, StorageInterface):
            raise NotImplementedError
        if path is not None:
            path = path
        else:
            path = "zcache.json"
        if StorageArgs is not None:
            if isinstance(StorageArgs, dict):
                self.storage = storage(path, **StorageArgs)
            else:
                raise TypeError
        else:
            self.storage = storage(path)
        self.__limit = limit

    def __updatefile(self):
        self.storage.save(self.databases)

    def __loadfile(self):
        self.databases = self.storage.load()
        self.databases["limit"] = self.__limit

    def __exists(self, key):
        try:
            t = self.databases["data"][key]
            if t["ttl"] != 0:
                sisa = int(time.time()) - t["time"]
                if sisa >= t["ttl"]:
                    if self.plugins is not None:
                        self.plugins.on_expired(self, key)
                    del self.databases["data"][key]
                    self.__updatefile()
                    return False, False
                else:
                    return True, t["content"]
            else:
                return True, t["content"]
        except KeyError:
            return False, False

    def __set(self, key, value, ttl=0):
        if self.plugins is not None:
            value = self.plugins.on_write(self, key, value)
        data = {}
        data["time"] = int(time.time())
        data["ttl"] = int(ttl)
        data["content"] = value
        self.databases["data"][key] = data
        self.__updatefile()

    def has(self, key):
        if not isinstance(key, str):
            raise TypeError
        self.__loadfile()
        r, v = self.__exists(key)
        return r

    def get(self, key):
        if not isinstance(key, str):
            raise TypeError
        self.__loadfile()
        r, v = self.__exists(key)
        if r:
            if self.plugins is not None:
                return self.plugins.on_read(self, key, v)
            return v
        else:
            return None

    def set(self, key, value, ttl=0):
        if not isinstance(key, str):
            raise TypeError
        # to optimize, __loadfile() not called here because already called in size()
        size = self.size()
        if self.databases["limit"] != 0:
            if self.databases["limit"] == size:
                if self.plugins is not None:
                    self.plugins.on_limit(self, key, value, ttl)
                return False
            else:
                self.__set(key, value, ttl)
                return True
        else:
            self.__set(key, value, ttl)
            return True

    def delete(self, key):
        if not isinstance(key, str):
            raise TypeError
        # to optimize, __loadfile() not called here because already called in has()
        check = self.has(key)
        if check:
            if self.plugins is not None:
                self.plugins.on_delete(self, key)
            del self.databases["data"][key]
            self.__updatefile()
            return True
        else:
            return False

    def size(self):
        self.__loadfile()
        ret = len(self.databases["data"])
        return ret

    def reset(self):
        self.__loadfile()
        self.databases["data"] = {}
        self.__updatefile()
