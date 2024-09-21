# -*-coding:utf8;-*-
from zcache.Storage.BaseFileStorage import BaseFileStorage
from zcache.Class.Database import Database
import uuid


class Queue:
    """Implementasi FIFO Queue.

    Methods:
    - put(item): Menambahkan item ke dalam queue.
    - get(): Menghapus dan mengembalikan item pertama dari queue.
    - peek(): Melihat item pertama tanpa menghapusnya.
    - empty(): Mengecek apakah queue kosong.
    - size(): Mendapatkan jumlah item dalam queue.
    """

    def __init__(self, path="queue.json", storage=BaseFileStorage, **kwargs):
        self.q = Database(path=path, storage=BaseFileStorage, **kwargs)
        self._stack_load()

    def put(self, item, id=str(uuid.uuid4())):
        """Menambahkan item ke dalam queue."""
        if not isinstance(id, str):
            raise TypeError
        if id == "__queue__":
            raise ValueError
        queue = self._stack_load()
        queue.append(id)
        a = self.q.set(id, item)
        if a:
            self._stack_update(queue)
            return id
        else:
            return None

    def get(self):
        """Menghapus dan mengembalikan item pertama dari queue."""
        queue = self._stack_load()
        if len(queue) > 0:
            id = queue.pop(0)
            ret = self.q.get(id)
            self.q.delete(id)
            self._stack_update(queue)
            return ret
        else:
            return None

    def peek(self):
        """Melihat item pertama tanpa menghapusnya."""
        queue = self._stack_load()
        if len(queue) > 0:
            id = queue[0]
            return self.q.get(id)

    def _stack_load(self):
        if not self.q.has("__queue__"):
            self.q.set("__queue__", [])
            return []
        return self.q.get("__queue__")

    def _stack_update(self, data):
        self.q.set("__queue__", data)

    def empty(self):
        """Mengecek apakah queue kosong."""
        queue = self._stack_load()
        return len(queue) == 0

    def size(self):
        """Mendapatkan jumlah item dalam queue."""
        queue = self._stack_load()
        return len(queue)

    def exists(self, id):
        """Mengecek id queue"""
        if not isinstance(id, str):
            raise TypeError
        queue = self._stack_load()
        return id in queue
