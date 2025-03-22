# -*-coding:utf8;-*-
from zcache.version import __version__
from zcache.Interface import StorageInterface
import time
import json
import os
from typing import Dict, Any


class BaseFileStorage(StorageInterface):
    def __init__(self, path: str) -> None:
        if not isinstance(path, str):
            raise TypeError
        if os.path.isdir(path):
            path = os.path.join(path, "zcache.json")
        self._path = path
        if not os.path.exists(path):
            self.create(path)

    @property
    def filesystem(self) -> bool:
        return True

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
        self.save(data)

    def load(self) -> Dict[str, Any]:
        with open(self._path, "r") as f:
            ret = json.loads(f.read())
        return dict(ret)

    def save(self, data: Dict[str, Any]) -> None:
        json_encoded = json.dumps(data)
        with open(self._path, "w") as f:
            f.write(json_encoded)
