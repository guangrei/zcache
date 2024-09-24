# -*- coding: utf-8 -*-
import unittest
from zcache.Class.Database import Database
import time


class DBTest(unittest.TestCase):

    def test_database_or_cache(self):
        c = Database("/tmp/test.cache")
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
        d = Database("/tmp/test2.cache", limit=2)
        d.reset()
        self.assertEqual(d.set("one", 1), True)
        self.assertEqual(d.set("two", 2), True)
        self.assertEqual(d.set("three", 3), False)
        self.assertEqual(d.delete("one"), True)
        self.assertEqual(d.set("three", 3), True)
