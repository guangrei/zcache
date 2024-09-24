# -*-coding:utf8;-*-
import aiofiles
from zcache.version import __version__
from zcache.Interface.Storage import Storage
import time
import json
import os
from asyncinit import asyncinit


@asyncinit
class AsyncFileStorage(Storage):

    filesystem = True

    async def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError
        if os.path.isdir(path):
            path = os.path.join(path, "zcache.json")
        if not os.path.exists(path):
            await self.create(path)
        self.path = path

    async def create(self, path):
        data = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = __version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        async with aiofiles.open(path, mode="w") as f:
            await f.write(json.dumps(data))

    async def load(self):
        async with aiofiles.open(self.path, mode="r") as f:
            data = await f.read()
        return json.loads(data)

    async def save(self, data):
        data = json.dumps(data)
        async with aiofiles.open(self.path, mode="w") as f:
            await f.write(data)
