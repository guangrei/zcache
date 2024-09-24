# -*-coding:utf8;-*-
import unittest
from zcache.Extras.Queue import Queue


class QueueTest(unittest.TestCase):
    def test_queue(self):
        q = Queue("/tmp/test_queue.json")
        id = q.put("test")
        self.assertEqual(q.exists(id), True)
        self.assertEqual(q.peek(), "test")
        self.assertEqual(q.size(), 1)
        self.assertEqual(q.empty(), False)
        self.assertEqual(q.get(), "test")
        self.assertEqual(q.size(), 0)
        self.assertEqual(q.empty(), True)
        self.assertEqual(q.exists(id), False)

    def test_queue_limit(self):
        q = Queue("/tmp/test_queue_limit.json", limit=2)
        id = q.put("test1")
        self.assertEqual(q.exists(id), True)
        id = q.put("test2")
        self.assertEqual(q.exists(id), True)
        id = q.put("test3")
        self.assertEqual(id, None)
