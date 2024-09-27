# -*- coding: utf-8 -*-
import unittest
from zcache.Class.Database import Database
from zcache.Storage.DictStorage import DictStorage


class DictStorageTest(unittest.TestCase):

    def test_database_or_cache(self):
        c = Database("/tmp/test_dict_storage.json", storage=DictStorage)
        c.reset()
        self.assertEqual(c.set("foo", "bar"), True)
        self.assertEqual(c.size(), 1)
