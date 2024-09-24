# -*-coding:utf8;-*-
from zcache.version import __version__
from zcache.Interface.Storage import Storage
import time
from asyncinit import asyncinit


@asyncinit
class AsyncDictStorage(Storage):
    database = {}
    filesystem = False

    async def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError
        if path not in self.database:
            await self.create(path)
        self.path = path

    async def create(self, path):
        data = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = __version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        self.database[path] = data

    async def load(self):
        return self.database[self.path]

    async def save(self, data):
        self.database[self.path] = data
