PyZCache is dependency free python key value cache based file storage and json serialize.

extra features:
- limit able stack cache
- option to add ttl (time to life) in cache content
- encryption (not yet implemented)

## Installation
```
pip install zcache
```
# example

basic example:
```python
from zcache import Cache
import time

c = Cache(path="/tmp")
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

d = Cache(path="/tmp", limit=2)
d.reset()  # reset cache stack to 0
print(d.set("one", 1))  # True
print(d.set("two", 2))  # True
print(d.set("three", 3))  # False out of stack limit
d.delete("one")  # delete one item from stack
print(d.set("three", 3))  # True
```
## License

MIT
