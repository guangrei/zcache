# -*-coding:utf8;-*-
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, Awaitable, Generator
from typing_extensions import Self


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
    def get(self, key: str, default: Any) -> Any:
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


class AsyncDatabaseInterface(ABC):
    """
    Interface for asynchronous Cache/Database.
    """

    _init_future: Awaitable[None]

    @abstractmethod
    def __init__(
        self,
        path: Optional[str] = None,
        limit: int = 0,
        storage: Optional["AsyncStorageInterface"] = None,
        plugins: Optional["AsyncPluginsInterface"] = None,
    ) -> None:
        """
        init method
        """
        pass

    @abstractmethod
    async def _constructor(self) -> Self:
        """
        async constructor
        """
        pass

    @abstractmethod
    def __await__(self) -> Generator[Any, None, Self]:
        """
        evaluate async constructor.
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
    def storage(self) -> "AsyncStorageInterface":
        """
        storage property, useful for plugins.
        """
        pass

    @abstractmethod
    async def has(self, key: str) -> bool:
        """
        check if key exists.
        """
        pass

    @abstractmethod
    async def get(self, key: str, default: Any) -> Any:
        """
        get value from key.
        """
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = 0) -> bool:
        """
        set key value to store.
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """
        delete value by key.
        """
        pass

    @abstractmethod
    async def size(self) -> int:
        """
        get database size.
        """
        pass

    @abstractmethod
    async def reset(self) -> None:
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


class AsyncStorageInterface(ABC):
    """
    Interface for asynchronous Storage.
    """

    _init_future: Awaitable[None]

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
    async def _constructor(self) -> Self:
        """
        async constructor
        """
        pass

    @abstractmethod
    def __await__(self) -> Generator[Any, None, Self]:
        """
        evaluate async constructor.
        """
        pass

    @abstractmethod
    async def load(self) -> Dict[str, Any]:
        """
        load data from storage.
        """
        pass

    @abstractmethod
    async def save(self, data: Dict[str, Any]) -> None:
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


class AsyncPluginsInterface(ABC):
    """
    Interface for asynchronous Plugins.
    """

    @abstractmethod
    async def on_write(self, db: "AsyncDatabaseInterface", key: str, value: Any) -> Any:
        """
        trigger at Database.__set()
        return will affect on data content before write.
        """
        pass

    @abstractmethod
    async def on_read(self, db: "AsyncDatabaseInterface", key: str, value: Any) -> Any:
        """
        trigger at Database.get()
        return will affect on data content after read.
        """
        pass

    @abstractmethod
    async def on_limit(
        self, db: "AsyncDatabaseInterface", key: str, value: Any, ttl: int
    ) -> None:
        """
        trigger when Database limit reached on Database.set()
        return will not affect anything.
        """
        pass

    @abstractmethod
    async def on_expired(self, db: "AsyncDatabaseInterface", key: str) -> None:
        """
        trigger when Database key time to live limit reached.
        return will not affect anything.
        """
        pass

    @abstractmethod
    async def on_delete(self, db: "AsyncDatabaseInterface", key: str) -> None:
        """
        trigger on Database.delete()
        return will not affect anything.
        """
        pass
