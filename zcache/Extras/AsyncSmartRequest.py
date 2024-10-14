# -*- coding: utf-8 -*-
from zcache.Core.AsyncDatabase import AsyncDatabase
from zcache.Plugins.AsyncBytesCachePlugins import AsyncBytesCachePlugins
import aiohttp
from typing import Any, Optional, Union, Dict


class AsyncSmartRequest:
    """
    A class for making Smart HTTP requests with caching capabilities using zcache
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._async_args = args
        self._async_kwargs = kwargs

    async def init(self) -> None:
        await self._init(*self._async_args, **self._async_kwargs)

    async def _init(
        self,
        url: Any,
        cache_path: Optional[str] = "smartrequest.json",
        cache_time: int = 120,
        offline_ttl: int = 604800,
        **kwargs: Any
    ) -> None:
        if not isinstance(url, str):
            cache_name = url.url
        else:
            cache_name = url
        plugins = AsyncBytesCachePlugins()
        cache = AsyncDatabase(path=cache_path, plugins=plugins, **kwargs)
        await cache.init()
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

    async def _makeRequest(
        self, url: Any, cache_name: str, cache: AsyncDatabase
    ) -> Union[Dict[str, Any], bool, None]:
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
