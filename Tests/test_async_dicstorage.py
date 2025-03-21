# -*- coding: utf-8 -*-
from unittest import IsolatedAsyncioTestCase
from zcache.Async import Cache
from zcache.Storage.AsyncDictStorage import AsyncDictStorage


class DBTest(IsolatedAsyncioTestCase):
    async def test_database_or_cache(self) -> None:
        storage = await AsyncDictStorage("test")
        c = await Cache(storage=storage)
        await c.reset()
        expected = await c.set("foo", "bar")
        self.assertEqual(expected, True)
