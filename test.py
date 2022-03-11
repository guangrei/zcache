# -*- coding: utf-8 -*-
from zcache import Cache
import time
import unittest

class CacheTest(unittest.TestCase):

	def test_cache(self):
		c = Cache()
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
		d = Cache(limit = 2)
		d.reset()
		self.assertEqual(d.set("one", 1), True)
		self.assertEqual(d.set("two", 2), True)
		self.assertEqual(d.set("three", 3), False)
		self.assertEqual(d.delete("one"), True)
		self.assertEqual(d.set("three", 3), True)

if __name__=="__main__":
	unittest.main()
	