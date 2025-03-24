# -*- coding: utf-8 -*-
import unittest
from zcache.Sync import Cache
from zcache.Storage.DictStorage import DictStorage


class DictStorageTest(unittest.TestCase):
    def test_database_or_cache(self) -> None:
        c = Cache(storage=DictStorage())
        c.reset()
        self.assertEqual(c.set("foo", "bar"), True)
        self.assertEqual(c.size(), 1)
