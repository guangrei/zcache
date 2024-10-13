# -*-coding:utf8;-*-
from zcache.Extras.AsyncSmartRequest import AsyncSmartRequest
from unittest import IsolatedAsyncioTestCase


class SmartRequestTest(IsolatedAsyncioTestCase):
    async def test_request(self) -> None:
        s = AsyncSmartRequest(
            "https://www.example.com", cache_path="/tmp/async_smart_request_test.json"
        )
        await s.init()
        self.assertEqual(s.is_loaded_from_cache, False)
        s = AsyncSmartRequest(
            "https://www.example.com", cache_path="/tmp/async_smart_request_test.json"
        )
        await s.init()
        self.assertEqual(s.is_loaded_from_cache, True)
