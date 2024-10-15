
[![status workflow test](https://github.com/guangrei/zcache/actions/workflows/python-app.yml/badge.svg)](https://github.com/guangrei/zcache/actions) 
[![status workflow build](https://github.com/guangrei/zcache/actions/workflows/release_to_pypi.yml/badge.svg)](https://github.com/guangrei/zcache/actions)

[![Downloads](https://static.pepy.tech/badge/zcache)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/month)](https://pepy.tech/project/zcache)
[![Downloads](https://static.pepy.tech/badge/zcache/week)](https://pepy.tech/project/zcache)

zcache is pure typed Python implementation of key value Cache/Database with abstract storage and plugins.

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

## Version Limited

version `2.0.2` is limited without Asynchronous and no need any dependency.

## License

MIT
