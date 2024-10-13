# -*- coding: utf-8 -*-
import unittest
from zcache.Class.Database import Database
from zcache.Storage.FcntlStorage import FcntlStorage


class FcntlStorageTest(unittest.TestCase):

    def test_database_or_cache(self) -> None:
        c = Database(storage=FcntlStorage("/tmp/test_fcntl_storage.json"))
        c.reset()
        self.assertEqual(c.set("foo", "bar"), True)
        self.assertEqual(c.size(), 1)
