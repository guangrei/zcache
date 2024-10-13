# -*-coding:utf8;-*-
from zcache.Extras.SmartRequest import SmartRequest
from typing import Tuple, Any, Dict
import unittest
import requests


class MyRequest:
    url = "https://www.example.com"

    @staticmethod
    def get() -> Tuple[Dict[str, str], bytes | Any]:
        r = requests.get(MyRequest.url)
        return dict(r.headers), r.content


class SmartRequestTest(unittest.TestCase):
    def test_request(self) -> None:
        s = SmartRequest(
            "https://www.example.com", cache_path="/tmp/smart_request_test1.json"
        )
        self.assertEqual(s.is_loaded_from_cache, False)
        s = SmartRequest(
            "https://www.example.com", cache_path="/tmp/smart_request_test1.json"
        )
        self.assertEqual(s.is_loaded_from_cache, True)
        r = SmartRequest(MyRequest, cache_path="/tmp/smart_request_test2.json")

        self.assertEqual(r.response["body"], s.response["body"])
