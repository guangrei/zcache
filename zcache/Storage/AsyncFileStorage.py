# -*-coding:utf8;-*-
import aiofiles
from zcache.version import __version__
from zcache.Interface import AsyncStorageInterface
import time
import json
import os
from typing import Dict, Any, Generator
from typing_extensions import Self


class AsyncFileStorage(AsyncStorageInterface):
    def __init__(self, path: str) -> None:
        self._path = path
        self._init_future = self._init()

    @property
    def filesystem(self) -> bool:
        return True

    @property
    def path(self) -> str:
        return self._path

    async def _init(self) -> None:
        path = self._path
        if os.path.isdir(path):
            path = os.path.join(path, "zcache.json")
        self._path = path
        if not os.path.exists(path):
            await self.create(path)

    async def _constructor(self) -> Self:
        await self._init_future
        return self

    def __await__(self) -> Generator[Any, None, Self]:
        return self._constructor().__await__()

    async def create(self, path: str) -> None:
        data: Dict[str, Any] = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = __version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        await self.save(data)

    async def load(self) -> Dict[str, Any]:
        async with aiofiles.open(self._path, mode="r") as f:
            data = await f.read()
        ret = json.loads(data)
        return dict(ret)

    async def save(self, data: Dict[str, Any]) -> None:
        json_encoded = json.dumps(data)
        async with aiofiles.open(self._path, mode="w") as f:
            await f.write(json_encoded)
