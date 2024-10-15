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
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict


class DatabaseInterface(ABC):
    """
    Interface for Cache/Database.
    """

    @abstractmethod
    def __init__(
        self,
        path: Optional[str] = None,
        limit: int = 0,
        storage: Optional["StorageInterface"] = None,
        plugins: Optional["PluginsInterface"] = None,
    ) -> None:
        """
        init method
        """
        pass

    @property
    @abstractmethod
    def databases(self) -> Dict[str, Any]:
        """
        Database property, useful for plugins.
        """
        pass

    @property
    @abstractmethod
    def storage(self) -> "StorageInterface":
        """
        storage property, useful for plugins.
        """
        pass

    @abstractmethod
    def has(self, key: str) -> bool:
        """
        check if key exists.
        """
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        """
        get value from key.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 0) -> bool:
        """
        set key value to store.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        delete value by key.
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """
        get database size.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        reset database to 0.
        """
        pass


class StorageInterface(ABC):
    """
    Interface for Storage.
    """

    @property
    @abstractmethod
    def filesystem(self) -> bool:
        """
        meta info, if storage is type filesystem or not.
        """
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        """
        meta info, get storage path.
        """
        pass

    @abstractmethod
    def __init__(self, path: str) -> None:
        """
        initialize storage.
        """
        pass

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """
        load data from storage.
        """
        pass

    @abstractmethod
    def save(self, data: Dict[str, Any]) -> None:
        """
        save data to storage.
        """
        pass


class PluginsInterface(ABC):
    """
    Interface for Plugins.
    """

    @abstractmethod
    def on_write(self, db: "DatabaseInterface", key: str, value: Any) -> Any:
        """
        trigger at Database.__set()
        return will affect on data content before write.
        """
        pass

    @abstractmethod
    def on_read(self, db: "DatabaseInterface", key: str, value: Any) -> Any:
        """
        trigger at Database.get()
        return will affect on data content after read.
        """
        pass

    @abstractmethod
    def on_limit(self, db: "DatabaseInterface", key: str, value: Any, ttl: int) -> None:
        """
        trigger when Database limit reached on Database.set()
        return will not affect anything.
        """
        pass

    @abstractmethod
    def on_expired(self, db: "DatabaseInterface", key: str) -> None:
        """
        trigger when Database key time to live limit reached.
        return will not affect anything.
        """
        pass

    @abstractmethod
    def on_delete(self, db: "DatabaseInterface", key: str) -> None:
        """
        trigger on Database.delete()
        return will not affect anything.
        """
        pass
