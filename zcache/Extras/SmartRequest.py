# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2022 zcache https://github.com/guangrei/zcache

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from zcache.Core.Database import Database
from zcache.Plugins.BytesCachePlugins import BytesCachePlugins
from urllib import request
from typing import Any, Optional, Union, Dict


class SmartRequest:
    """
    A class for making Smart HTTP requests with caching capabilities using PyZCache.
    """

    def __init__(
        self,
        url: Any,
        cache_path: Optional[str] = "smartrequest.json",
        cache_time: int = 120,
        offline_ttl: int = 604800,
        **kwargs: Any,
    ) -> None:
        if not isinstance(url, str):
            cache_name = url.url
        else:
            cache_name = url
        cache = Database(path=cache_path, plugins=BytesCachePlugins(), **kwargs)
        if cache.has(cache_name):
            self.response = cache.get(cache_name)
            self.is_loaded_from_cache = True
        else:
            r = self._makeRequest(url, cache_name, cache)
            if r is not False:
                cache.set(cache_name, r, ttl=cache_time)
                cache.set(cache_name + "_offline", r, ttl=offline_ttl)
                self.response = r
                self.is_loaded_from_cache = False
            else:
                self.response = cache.get(cache_name + "_offline")
                self.is_loaded_from_cache = True

    def _makeRequest(
        self, url: Any, cache_name: str, cache: Database
    ) -> Union[Dict[str, Any], bool, None]:
        if not isinstance(url, str):
            try:
                headers, body = url.get()
                return {"headers": headers, "body": body}
            except BaseException as e:
                if cache.has(cache_name + "_offline"):
                    return False
                else:
                    raise Exception(e)
        try:
            response = request.urlopen(url)
            headers, body = (dict(response.info()), response.read())
            return {"headers": headers, "body": body}
        except BaseException as e:
            if cache.has(cache_name + "_offline"):
                return False
            else:
                raise Exception(e)
