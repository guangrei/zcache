# -*- coding: utf-8 -*-
from zcache import Cache, SmartRequest, Queue
import requests
import time
import unittest


class MyRequest:
    url = "https://www.example.com"

    def get():
        r = requests.get(MyRequest.url)
        return dict(r.headers), r.content


class CacheTest(unittest.TestCase):

    def test_cache(self):
        c = Cache('/tmp/test.cache')
        c.reset()
        self.assertEqual(c.set("foo", "bar"), True)
        self.assertEqual(c.size(), 1)
        self.assertEqual(c.has("foo"), True)
        self.assertEqual(c.get("foo"), "bar")
        self.assertEqual(c.delete("foo"), True)
        self.assertEqual(c.has("foo"), False)
        self.assertEqual(c.set("spam", "eggs", ttl=3), True)
        self.assertEqual(c.has("spam"), True)
        time.sleep(3)
        self.assertEqual(c.has("spam"), False)
        self.assertEqual(c.size(), 0)

    def test_limit(self):
        d = Cache('/tmp/test2.cache', limit=2)
        d.reset()
        self.assertEqual(d.set("one", 1), True)
        self.assertEqual(d.set("two", 2), True)
        self.assertEqual(d.set("three", 3), False)
        self.assertEqual(d.delete("one"), True)
        self.assertEqual(d.set("three", 3), True)

    def test_request(self):

        r = SmartRequest(MyRequest, cache_path='/tmp/request1.cache')
        s = SmartRequest('https://www.example.com',
                         cache_path='/tmp/request2.cache')
        self.assertEqual(r.response["body"], s.response["body"])

    def test_queue(self):
        q = Queue()
        id = q.put("test")
        self.assertEqual(q.exists(id), True)
        self.assertEqual(q.peek(), "test")
        self.assertEqual(q.size(), 1)
        self.assertEqual(q.empty(), False)
        self.assertEqual(q.get(), "test")
        self.assertEqual(q.size(), 0)
        self.assertEqual(q.empty(), True)
        self.assertEqual(q.exists(id), False)
        

if __name__ == "__main__":
    unittest.main()
