# -*-coding:utf8;-*-
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

import aiofiles
from zcache.version import __version__
from zcache.Interface import AsyncStorageInterface
import time
import json
import os
from typing import Dict, Any


class AsyncFileStorage(AsyncStorageInterface):
    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def filesystem(self) -> bool:
        return True

    @property
    def path(self) -> str:
        return self._path

    async def init(self) -> None:
        await self._init(path=self._path)

    async def _init(self, path: str) -> None:
        if os.path.isdir(path):
            path = os.path.join(path, "zcache.json")
        self._path = path
        if not os.path.exists(path):
            await self.create(path)

    async def create(self, path: str) -> None:
        data: Dict[str, Any] = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = __version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        await self.save(data)

    async def load(self) -> Dict[str, Any]:
        async with aiofiles.open(self._path, mode="r") as f:
            data = await f.read()
        ret = json.loads(data)
        return dict(ret)

    async def save(self, data: Dict[str, Any]) -> None:
        json_encoded = json.dumps(data)
        async with aiofiles.open(self._path, mode="w") as f:
            await f.write(json_encoded)
