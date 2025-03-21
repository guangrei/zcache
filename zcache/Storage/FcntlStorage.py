# -*-coding:utf8;-*-
from zcache.version import __version__
from zcache.Interface import StorageInterface
from typing import IO, Optional, Type, Any, Dict
import time
import json
import fcntl
import os
from types import TracebackType


class FileLock:
    def __init__(self, filename: str, mode: str) -> None:
        self.filename = filename
        self.mode = mode

    def __enter__(self) -> IO[Any]:
        self.file_handle = open(self.filename, self.mode, encoding="utf-8")
        fcntl.flock(self.file_handle, fcntl.LOCK_EX)
        self.file_handle.seek(0)
        return self.file_handle

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        fcntl.flock(self.file_handle, fcntl.LOCK_UN)
        self.file_handle.close()


class FcntlStorage(StorageInterface):
    def __init__(self, path: str) -> None:
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
        with FileLock(self._path, mode="r") as f:
            data = json.loads(f.read())
        return dict(data)

    def save(self, data: Dict[str, Any]) -> None:
        json_encoded = json.dumps(data)
        with FileLock(self._path, mode="w") as f:
            f.write(json_encoded)
