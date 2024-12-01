# -*- coding: utf-8 -*-
from unittest import IsolatedAsyncioTestCase
from zcache.Core.AsyncDatabase import AsyncDatabase
import asyncio


class DBTest(IsolatedAsyncioTestCase):
    async def test_database_or_cache(self) -> None:
        c = AsyncDatabase("/tmp/async_cache_test.json")
        await c.init()
        await c.reset()

        expected = await c.set("foo", "bar")
        self.assertEqual(expected, True)

        expected_int = await c.size()
        self.assertEqual(expected_int, 1)

        expected = await c.has("foo")
        self.assertEqual(expected, True)

        expected = await c.get("foo")
        self.assertEqual(expected, "bar")

        expected = await c.delete("foo")
        self.assertEqual(expected, True)

        expected = await c.has("foo")
        self.assertEqual(expected, False)

        expected = await c.set("spam", "eggs", ttl=3)
        self.assertEqual(expected, True)

        expected = await c.has("spam")
        self.assertEqual(expected, True)

        await asyncio.sleep(3)

        expected = await c.has("spam")
        self.assertEqual(expected, False)

        expected_int = await c.size()
        self.assertEqual(expected_int, 0)

    async def test_limit(self) -> None:
        d = AsyncDatabase("/tmp/async_cache_test.json", limit=2)
        await d.init()
        await d.reset()

        expected = await d.set("one", 1)
        self.assertEqual(expected, True)

        expected = await d.set("two", 2)
        self.assertEqual(expected, True)

        expected = await d.set("three", 3)
        self.assertEqual(expected, False)

        expected = await d.delete("one")
        self.assertEqual(expected, True)

        expected = await d.set("three", 3)
        self.assertEqual(expected, True)
