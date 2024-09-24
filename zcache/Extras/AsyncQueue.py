# -*-coding:utf8;-*-
from zcache.Storage.AsyncFileStorage import AsyncFileStorage
from zcache.Class.AsyncDatabase import AsyncDatabase
import uuid
from asyncinit import asyncinit


@asyncinit
class AsyncQueue:
    """Implementasi FIFO Queue.

    Methods:
    - put(item): Menambahkan item ke dalam queue.
    - get(): Menghapus dan mengembalikan item pertama dari queue.
    - peek(): Melihat item pertama tanpa menghapusnya.
    - empty(): Mengecek apakah queue kosong.
    - size(): Mendapatkan jumlah item dalam queue.
    """

    async def __init__(
        self, path="queue.json", storage=AsyncFileStorage, limit=0, **kwargs
    ):
        self.limit = limit
        self.q = await AsyncDatabase(path=path, storage=storage, **kwargs)
        await self._stack_load()

    async def put(self, item, id=str(uuid.uuid4())):
        """Menambahkan item ke dalam queue."""
        if not isinstance(id, str):
            raise TypeError
        if id == "__queue__":
            raise ValueError
        queue = await self._stack_load()
        if self.limit > 0:
            if len(queue) < self.limit:
                queue.append(id)
                await self.q.set(id, item)
                await self._stack_update(queue)
                return id
            else:
                return None
        else:
            queue.append(id)
            await self.q.set(id, item)
            await self._stack_update(queue)
            return id

    async def get(self):
        """Menghapus dan mengembalikan item pertama dari queue."""
        queue = await self._stack_load()
        if len(queue) > 0:
            id = queue.pop(0)
            ret = await self.q.get(id)
            await self.q.delete(id)
            await self._stack_update(queue)
            return ret
        else:
            return None

    async def peek(self):
        """Melihat item pertama tanpa menghapusnya."""
        queue = await self._stack_load()
        if len(queue) > 0:
            id = queue[0]
            ret = await self.q.get(id)
            return ret

    async def _stack_load(self):
        check = await self.q.has("__queue__")
        if not check:
            await self.q.set("__queue__", [])
            return []
        ret = await self.q.get("__queue__")
        return ret

    async def _stack_update(self, data):
        await self.q.set("__queue__", data)

    async def empty(self):
        """Mengecek apakah queue kosong."""
        queue = await self._stack_load()
        return len(queue) == 0

    async def size(self):
        """Mendapatkan jumlah item dalam queue."""
        queue = await self._stack_load()
        return len(queue)

    async def exists(self, id):
        """mengecek id queue"""
        if not isinstance(id, str):
            raise TypeError
        queue = await self._stack_load()
        return id in queue
