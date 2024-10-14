# -*- coding: utf-8 -*-
from unittest import IsolatedAsyncioTestCase
from zcache.Core.AsyncDatabase import AsyncDatabase
from zcache.Storage.AsyncDictStorage import AsyncDictStorage


class DBTest(IsolatedAsyncioTestCase):

    async def test_database_or_cache(self) -> None:
        storage = AsyncDictStorage("test")
        await storage.init()
        c = AsyncDatabase(storage=storage)
        await c.init()
        await c.reset()
        expected = await c.set("foo", "bar")
        self.assertEqual(expected, True)
