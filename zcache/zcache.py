# -*-coding:utf8;-*-
"""
The MIT License (MIT)

Copyright (c) 2022 PyZCache https://github.com/guangrei/PyZCache

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

import os
import sys
import time
import json


class Cache(object):
    """
    PyZCache is dependency less python key value cache based file storage and json serialize.
    """
    __version__ = "0.01"

    def __init__(self, path=None, limit=0, encryption=None):
        if path is not None:
            path = path
        else:
            path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.__path = path
        if not os.path.exists(path+"/.PyZCache"):
            self.__mkfile(path)
        self.__limit = limit

    def __loadfile(self):
        with open(self.__path+"/.PyZCache", "r") as f:
            self.__data = json.loads(f.read())
            self.__data["limit"] = self.__limit

    def __mkfile(self, path):
        data = {}
        data["file"] = "PyZCache"
        data["first created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = self.__version__
        data["url"] = "https://github.com/guangrei/PyZCache"
        data["cache"] = {}
        data["limit"] = 0
        with open(path+"/.PyZCache", "w") as f:
            f.write(json.dumps(data))

    def __updatefile(self):
        data = json.dumps(self.__data)
        with open(self.__path+"/.PyZCache", "w") as f:
            f.write(data)
        return True

    def __exists(self, key):
        key = str(key)
        try:
            t = self.__data["cache"][key]
            if(t["ttl"] != 0):
                sisa = int(time.time())-t["time"]
                if sisa >= t["ttl"]:
                    del self.__data["cache"][key]
                    self.__updatefile()
                    return False, False
                else:
                    return True, t["content"]
            else:
                return True, t["content"]
        except KeyError:
            return False, False

    def __set(self, key, value, ttl=0):
        key = str(key)
        data = {}
        data["time"] = int(time.time())
        data["ttl"] = int(ttl)
        data["content"] = value
        self.__data["cache"][key] = data
        self.__updatefile()

    def has(self, key):
        key = str(key)
        self.__loadfile()
        r, v = self.__exists(key)
        return r

    def get(self, key):
        key = str(key)
        self.__loadfile()
        r, v = self.__exists(key)
        if r:
            return v
        else:
            return False

    def set(self, key, value, ttl=0):
        key = str(key)
        # to optimize, __loadfile() not called here because already called in size()
        size = self.size()
        if self.__data["limit"] != 0:
            if self.__data["limit"] == size:
                return False
            else:
                self.__set(key, value, ttl)
                return True
        else:
            self.__set(key, value, ttl)
            return True

    def delete(self, key):
        key = str(key)
        # to optimize, __loadfile() not called here because already called in has()
        check = self.has(key)
        if check:
            del self.__data["cache"][key]
            self.__updatefile()
            return True
        else:
            return False

    def size(self):
        self.__loadfile()
        ret = len(self.__data["cache"])
        return ret

    def reset(self):
        self.__loadfile()
        self.__data["cache"] = {}
        self.__updatefile()


if __name__ == "__main__":
    pass
