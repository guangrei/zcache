# -*-coding:utf8;-*-
from unittest import IsolatedAsyncioTestCase
from zcache.Extras.AsyncQueue import AsyncQueue


class QueueTest(IsolatedAsyncioTestCase):
    async def test_queue(self) -> None:
        q = AsyncQueue(path="/tmp/test_async_queue.json")
        await q.init()
        id = await q.put("test")
        expected = await q.exists(id)
        self.assertEqual(expected, True)
        expected = await q.peek()
        self.assertEqual(expected, "test")
        expected_int = await q.size()
        self.assertEqual(expected_int, 1)
        expected = await q.empty()
        self.assertEqual(expected, False)
        expected = await q.get()
        self.assertEqual(expected, "test")
        expected_int = await q.size()
        self.assertEqual(expected_int, 0)
        expected = await q.empty()
        self.assertEqual(expected, True)
        expected = await q.exists(id)
        self.assertEqual(expected, False)

    async def test_queue_limit(self) -> None:
        q = AsyncQueue(path="/tmp/test_async_queue_limit.json", limit=2)
        await q.init()
        id = await q.put("test1")
        expected = await q.exists(id)
        self.assertEqual(expected, True)
        id = await q.put("test2")
        expected = await q.exists(id)
        self.assertEqual(expected, True)
        id = await q.put("test3")
        self.assertEqual(id, None)

    async def test_queue_id(self) -> None:
        q = AsyncQueue(path="/tmp/test_async_queue_id.json")
        await q.init()
        id = await q.put("test", id="test123")
        expected = await q.exists(id)
        self.assertEqual(expected, True)
        self.assertEqual(id, "test123")
