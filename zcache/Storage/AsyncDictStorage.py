# -*-coding:utf8;-*-
from zcache.version import __version__
from zcache.Interface import AsyncStorageInterface
import time
from typing import Dict, Any, Generator
from typing_extensions import Self


class AsyncDictStorage(AsyncStorageInterface):
    database: Dict[str, Dict[str, Any]] = {}

    def __init__(self, path: str = "zcache.json") -> None:
        self._path = path
        self._init_future = self._init()

    @property
    def filesystem(self) -> bool:
        return False

    @property
    def path(self) -> str:
        return self._path

    async def _init(self) -> None:
        if self._path not in self.database:
            await self.create(self._path)

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
        self.database[path] = data

    async def load(self) -> Dict[str, Any]:
        return self.database[self._path]

    async def save(self, data: Dict[str, Any]) -> None:
        self.database[self._path] = data
