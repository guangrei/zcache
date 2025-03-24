# -*-coding:utf8;-*-
from zcache.version import __version__
from zcache.Interface import StorageInterface
from typing import Dict, Any
import time


class DictStorage(StorageInterface):
    database: Dict[str, Dict[str, Any]] = {}

    def __init__(self, path: str = "zcache.json") -> None:
        if path not in self.database:
            self.create(path)
        self._path = path

    @property
    def filesystem(self) -> bool:
        return False

    @property
    def path(self) -> str:
        return self._path

    def create(self, path: str) -> None:
        data: Dict[str, Any] = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = __version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        self.database[path] = data

    def load(self) -> Dict[str, Any]:
        return self.database[self._path]

    def save(self, data: Dict[str, Any]) -> None:
        self.database[self._path] = data
