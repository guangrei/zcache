[![status workflow test](https://github.com/guangrei/PyZcache/actions/workflows/python-app.yml/badge.svg)](https://github.com/guangrei/PyZcache/actions) 
[![status workflow build](https://github.com/guangrei/PyZcache/actions/workflows/release_to_pypi.yml/badge.svg)](https://github.com/guangrei/PyZcache/actions)

[![Downloads](https://static.pepy.tech/badge/zcache)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/month)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/week)](https://pepy.tech/project/zcache)

PyZCache is dependency free python key value cache based file storage and json serialize.

extra features:
- limit able stack cache
- option to add ttl (time to life) in cache content
- smart request

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

# SmartRequest

`SmartRequest` is Simple HTTP Client with smart caching system provide by `zcache`.

example usage of `SmartRequest(url, cache_path, cache_time, offline_ttl)`:
```python
from zcache import SmartRequest

req = SmartRequest("https://www.example.com", cache_path="/tmp/request1.cache")
print(req.is_loaded_from_cache) # check if response is loaded from cache
response_headers = req.response.get('headers')
response_body = req.response.get('body')
```
to make advance request you can create custom url object with other library, for example:
```python
from zcache import SmartRequest
import requests

class MyRequest:
    url = "https://www.example.com"
    
    def get():
        """
        this method called by SmartRequest to retrieve content.
        you can put request logic get, post etc and return tuple(headers=dict, body=str)
        """
        
        ret = requests.get(MyRequest.url)
        return dict(ret.headers), ret.text


req = SmartRequest(MyRequest, cache_path="/tmp/request2.cache")
```
note: caching for request media/binary content is possible with `base64` encode. 
## License

MIT
