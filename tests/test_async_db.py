# -*- coding: utf-8 -*-
from unittest import IsolatedAsyncioTestCase
from zcache.Class.AsyncDatabase import AsyncDatabase
import asyncio


class DBTest(IsolatedAsyncioTestCase):

    async def test_database_or_cache(self):
        c = await AsyncDatabase("/tmp/async_cache_test.json")
        await c.reset()

        expected = await c.set("foo", "bar")
        self.assertEqual(expected, True)

        expected = await c.size()
        self.assertEqual(expected, 1)

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

        expected = await c.size()
        self.assertEqual(expected, 0)

    async def test_limit(self):
        d = await AsyncDatabase("/tmp/async_cache_test.json", limit=2)
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
