[![status workflow test](https://github.com/guangrei/zcache/actions/workflows/python-app.yml/badge.svg)](https://github.com/guangrei/zcache/actions) 
[![status workflow build](https://github.com/guangrei/zcache/actions/workflows/release_to_pypi.yml/badge.svg)](https://github.com/guangrei/zcache/actions)

[![Downloads](https://static.pepy.tech/badge/zcache)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/month)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/week)](https://pepy.tech/project/zcache)

zcache is pure python implementation of key value Cache/Database with abstract storage and plugins support.

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

# Storage and plugins

you can change storage and use plugins, for example:

```python
from zcache import Cache
from zcache.Plugins.BytesCachePlugins import BytesCachePlugins
from zcache.Storage.BaseFileStorage import BaseFileStorage

c = Cache(storage=BaseFileStorage, plugins=BytesCachePlugins)
```
see list current available [storage](https://github.com/guangrei/zcache/tree/main/zcache/Storage) and [plugins](https://github.com/guangrei/zcache/tree/main/zcache/Plugins), you can also create your own storage and plugins.

## Extras

[extras](https://github.com/guangrei/zcache/tree/main/zcache/Extras) is several function based on zcache.

1. SmartRequest

`SmartRequest` is Simple HTTP Client with smart caching system provide by `zcache`.

example usage of `SmartRequest(url, cache_path, cache_time, offline_ttl)`:
```python
from zcache.Extras.SmartRequest import SmartRequest

req = SmartRequest("https://www.example.com", cache_path="/tmp/request1.cache")
print(req.is_loaded_from_cache) # check if response is loaded from cache
response_headers = req.response.get('headers')
response_body = req.response.get('body')
```
to make advance request you can create custom url object with other library, for example:
```python
from zcache.Extras.SmartRequest import SmartRequest

class MyRequest:
    url = "https://www.example.com"
    
    def get():
        """
        this method called by SmartRequest to retrieve content.
        you can put request logic get, post etc and return tuple(headers=dict, body=str/bytes)
        """
        
        ret = requests.get(MyRequest.url)
        return dict(ret.headers), ret.content


req = SmartRequest(MyRequest, cache_path="/tmp/request2.cache")
```

> from zcache 1.0.3 SmartRequest body support str & bytes and already use BytesCachePlugins to store large file/content.

2. Queue

```python
from zcache.Extras.Queue import Queue

q = Queue()
q.put("test", id="123") # id must be a string and optional (default random uuid)
q.exists("123")
q.peek() # view top item  without enqueue
q.empty()
q.size()
q.get()
```

## License

MIT
