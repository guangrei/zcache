# -*-coding:utf8;-*-
from zcache.Extras.AsyncSmartRequest import AsyncSmartRequest
from unittest import IsolatedAsyncioTestCase


class SmartRequestTest(IsolatedAsyncioTestCase):
    async def test_request(self):
        s = await AsyncSmartRequest(
            "https://www.example.com", cache_path="/tmp/async_smart_request_test.json"
        )
        self.assertEqual(s.is_loaded_from_cache, False)
        s = await AsyncSmartRequest(
            "https://www.example.com", cache_path="/tmp/async_smart_request_test.json"
        )
        self.assertEqual(s.is_loaded_from_cache, True)
