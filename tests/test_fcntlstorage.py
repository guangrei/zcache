# -*- coding: utf-8 -*-
import unittest
from zcache.Class.Database import Database
from zcache.Storage.FcntlStorage import FcntlStorage


class FcntlStorageTest(unittest.TestCase):

    def test_database_or_cache(self):
        c = Database("/tmp/test_fcntl_storage.json", storage=FcntlStorage)
        c.reset()
        self.assertEqual(c.set("foo", "bar"), True)
        self.assertEqual(c.size(), 1)
