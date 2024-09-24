# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2022 PyZCache https://github.com/guangrei/PyZCache

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
from zcache.Class.AsyncDatabase import AsyncDatabase
from zcache.Plugins.AsyncBytesCachePlugins import AsyncBytesCachePlugins
from asyncinit import asyncinit
import aiohttp


@asyncinit
class AsyncSmartRequest:
    """
    A class for making Smart HTTP requests with caching capabilities using PyZCache.
    """

    async def __init__(
        self,
        url,
        cache_path="smartrequest.json",
        cache_time=120,
        offline_ttl=604800,
        **kwargs
    ):
        if not isinstance(url, str):
            cache_name = url.url
        else:
            cache_name = url
        cache = await AsyncDatabase(
            path=cache_path, plugins=AsyncBytesCachePlugins, **kwargs
        )
        cek = await cache.has(cache_name)
        if cek:
            self.response = await cache.get(cache_name)
            self.is_loaded_from_cache = True
        else:
            r = await self._makeRequest(url, cache_name, cache)
            if r is not False:
                await cache.set(cache_name, r, ttl=cache_time)
                await cache.set(cache_name + "_offline", r, ttl=offline_ttl)
                self.response = r
                self.is_loaded_from_cache = False
            else:
                self.response = await cache.get(cache_name + "_offline")
                self.is_loaded_from_cache = True

    async def _makeRequest(self, url, cache_name, cache):
        if not isinstance(url, str):
            try:
                headers, body = await url.get()
                return {"headers": headers, "body": body}
            except BaseException as e:
                cek = await cache.has(cache_name + "_offline")
                if cek:
                    return False
                else:
                    raise Exception(e)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    ret = await resp.read()
            headers, body = (dict(resp.headers), ret)
            return {"headers": headers, "body": body}
        except BaseException as e:
            cek = await cache.has(cache_name + "_offline")
            if cek:
                return False
            else:
                raise Exception(e)
