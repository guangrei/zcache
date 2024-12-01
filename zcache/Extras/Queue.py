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

from zcache.Core.Database import Database
import uuid
from zcache.Interface import StorageInterface
from typing import Any, Optional, Union, List
from typing_extensions import Never


class Queue:
    """Implementasi FIFO Queue.

    Methods:
    - put(item): Menambahkan item ke dalam queue.
    - get(): Menghapus dan mengembalikan item pertama dari queue.
    - peek(): Melihat item pertama tanpa menghapusnya.
    - empty(): Mengecek apakah queue kosong.
    - size(): Mendapatkan jumlah item dalam queue.
    """

    def __init__(
        self,
        path: Optional[str] = "queue.json",
        storage: Optional[StorageInterface] = None,
        limit: int = 0,
        **kwargs: Any,
    ) -> None:
        self.limit = limit
        self.q = Database(path=path, storage=storage, **kwargs)
        self._stack_load()

    def put(self, item: Any, id: str = str(uuid.uuid4())) -> Union[str, None]:
        """Menambahkan item ke dalam queue."""
        if id == "__queue__":
            raise ValueError
        queue = self._stack_load()
        if self.limit > 0:
            if len(queue) < self.limit:
                queue.append(id)
                self.q.set(id, item)
                self._stack_update(queue)
                return id
            else:
                return None
        else:
            queue.append(id)
            self.q.set(id, item)
            self._stack_update(queue)
            return id

    def get(self) -> Any:
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

    def peek(self) -> Any:
        """Melihat item pertama tanpa menghapusnya."""
        queue = self._stack_load()
        if len(queue) > 0:
            id = queue[0]
            return self.q.get(id)

    def _stack_load(self) -> List[Union[Never, str]]:
        if not self.q.has("__queue__"):
            self.q.set("__queue__", [])
            return []
        return self.q.get("__queue__")  # type: ignore[no-any-return]

    def _stack_update(self, data: List[Union[Never, str]]) -> None:
        self.q.set("__queue__", data)

    def empty(self) -> bool:
        """Mengecek apakah queue kosong."""
        queue = self._stack_load()
        return len(queue) == 0

    def size(self) -> int:
        """Mendapatkan jumlah item dalam queue."""
        queue = self._stack_load()
        return len(queue)

    def exists(self, id: Optional[str] = None) -> bool:
        """Mengecek id queue"""
        queue = self._stack_load()
        return id in queue
