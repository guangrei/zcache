# -*- coding: utf-8 -*-
from unittest import IsolatedAsyncioTestCase
from zcache.Class.AsyncDatabase import AsyncDatabase
from zcache.Storage.AsyncDictStorage import AsyncDictStorage


class DBTest(IsolatedAsyncioTestCase):

    async def test_database_or_cache(self):
        c = await AsyncDatabase("/tmp/async_dicstorage_test.json", storage=AsyncDictStorage)
        await c.reset()

        expected = await c.set("foo", "bar")
        self.assertEqual(expected, True)