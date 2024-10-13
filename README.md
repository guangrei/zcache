
[![status workflow test](https://github.com/guangrei/zcache/actions/workflows/python-app.yml/badge.svg)](https://github.com/guangrei/zcache/actions) 
[![status workflow build](https://github.com/guangrei/zcache/actions/workflows/release_to_pypi.yml/badge.svg)](https://github.com/guangrei/zcache/actions)

[![Downloads](https://static.pepy.tech/badge/zcache)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/month)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/week)](https://pepy.tech/project/zcache)

zcache is pure typed Python implementation of key value Cache/Database with abstract storage, plugins and asynchronous support.

## Installation
```
pip install zcache
```
# example

basic example:
```python
from zcache import Cache
import time

c = Cache(path="/tmp/tes1.cache")
print("set foo=bar: ", c.set("foo", "bar"))
print("c size:", c.size())
print("c has foo: ", c.has("foo"))
print("c get foo: ", c.get("foo"))
print("c delete foo: ", c.delete("foo"))
print("c has foo: ", c.has("foo"))
print("c has spam:", c.has("spam"))
print("c set spam=eggs, ttl=3: ", c.set("spam", "eggs", ttl=3)) # cache with ttl
print("c has spam:", c.has("spam"))
print("sleep 3")
time.sleep(3)
print("c has spam:", c.has("spam"))
print("c size:", c.size())
```
example with limited stack:
```python
from zcache import Cache

d = Cache(path="/tmp/test2.cache", limit=2)
d.reset()  # reset cache stack to 0
print(d.set("one", 1))  # True
print(d.set("two", 2))  # True
print(d.set("three", 3))  # False out of stack limit
d.delete("one")  # delete one item from stack
print(d.set("three", 3))  # True
```

# Asynchronous

example asynchronous usage

```python
import asyncio
from zcache import AsyncCache

async def main():
    c = AsyncCache()
    await c.init()
    await c.set("test", "OK")
    print(await c.get("test"))

if __name__ == '__main__':
    asyncio.run(main())
```

# Storage and plugins

you can change storage and use plugins, for example:

```python
from zcache import Cache
from zcache.Plugins.BytesCachePlugins import BytesCachePlugins
from zcache.Storage.BaseFileStorage import BaseFileStorage


storage = BaseFileStorage("/tmp/zcache.json")
plugins = BytesCachePlugins()
c = Cache(storage=storage, plugins=plugins)
```
see list current available [storage](https://github.com/guangrei/zcache/tree/main/zcache/Storage) and [plugins](https://github.com/guangrei/zcache/tree/main/zcache/Plugins), you can also create your own storage and plugins.

# Extras

[Extras](https://github.com/guangrei/zcache/tree/main/zcache/Extras) is several module based on zcache.

1. [SmartRequest](https://github.com/guangrei/zcache/blob/main/Tests/test_smartrequest.py)

`SmartRequest` is Simple HTTP Client with smart caching system based on `zcache`.

2.[AsyncSmartRequest](https://github.com/guangrei/zcache/blob/main/Tests/test_async_smartrequest.py)

`AsyncSmartRequest` is asynchronous version of `SmartRequests`.

3. [Queue](https://github.com/guangrei/zcache/blob/main/Tests/test_queue.py)

`Queue` is Fifo Queue based on `zcache`.

4. [AsyncQueue](https://github.com/guangrei/zcache/blob/main/Tests/test_async_queue.py)

`AsyncQueue` is asynchronous version of`zcache`.


## License

MIT
