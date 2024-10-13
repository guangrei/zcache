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
from zcache.Interface import PluginsInterface, DatabaseInterface
from typing import Any
import pickle
import os


class BytesCachePlugins(PluginsInterface):
    """
    this plugins is good for large cache and can store any python object
    """

    def __init__(self) -> None:
        self.useRandomName = True

    def on_write(self, db: DatabaseInterface, key: str, value: Any) -> Any:  # noqa
        if db.storage.filesystem:
            path = os.path.dirname(db.storage.path)
            darray = db.databases
            if key in darray["data"]:
                filepath = darray["data"][key]["content"]
                if isinstance(filepath, str):
                    if filepath.startswith("pickle://"):
                        filepath = filepath[9:]
                    elif filepath.startswith("bytes://"):
                        filepath = filepath[8:]
                    elif filepath.startswith("text://"):
                        filepath = filepath[7:]
                    else:
                        return value
                else:
                    return value

                if isinstance(value, bytes):
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, value)
                    else:
                        self.write(filepath, value)
                    return "bytes://" + filepath
                elif isinstance(value, str):
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, value.encode("utf-8"))
                    else:
                        self.write(filepath, value.encode("utf-8"))
                    return "text://" + filepath
                else:
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, self.pickle_encode(value))
                    else:
                        self.write(filepath, self.pickle_encode(value))
                    return "pickle://" + filepath
            else:
                if self.useRandomName:
                    import uuid

                    filename = ".zcache-" + uuid.uuid4().hex
                else:
                    filename = ".zcache-" + key
                filepath = os.path.join(path, filename)
                if isinstance(value, bytes):
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, value)
                    else:
                        self.write(filepath, value)
                    return "bytes://" + filepath
                elif isinstance(value, str):
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, value.encode("utf-8"))
                    else:
                        self.write(filepath, value.encode("utf-8"))
                    return "text://" + filepath
                else:
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, self.pickle_encode(value))
                    else:
                        self.write(filepath, self.pickle_encode(value))
                    return "pickle://" + filepath
        else:
            return value

    def on_read(self, db: DatabaseInterface, key: str, value: Any) -> Any:
        if db.storage.filesystem:
            if isinstance(value, str):
                filepath = value
                if filepath.startswith("pickle://"):
                    if hasattr(db.storage, "read"):
                        ret = db.storage.read(filepath[9:])
                    else:
                        ret = self.read(filepath[9:])
                    return self.pickle_decode(ret)
                elif filepath.startswith("text://"):
                    if hasattr(db.storage, "read"):
                        ret = db.storage.read(filepath[7:])
                    else:
                        ret = self.read(filepath[7:])
                    return ret.decode("utf-8")
                elif filepath.startswith("bytes://"):
                    if hasattr(db.storage, "read"):
                        return db.storage.read(filepath[8:])
                    else:
                        return self.read(filepath[8:])
                else:
                    return value
            else:
                return value
        else:
            return value

    def on_limit(self, db: DatabaseInterface, key: str, value: Any, ttl: int) -> None:
        pass

    def on_expired(self, db: DatabaseInterface, key: str) -> None:
        if db.storage.filesystem:
            filepath = db.databases["data"][key]["content"]
            if isinstance(filepath, str):
                if filepath.startswith("pickle://"):
                    filepath = filepath[9:]
                elif filepath.startswith("bytes://"):
                    filepath = filepath[8:]
                elif filepath.startswith("text://"):
                    filepath = filepath[7:]
                else:
                    return
                if hasattr(db.storage, "delete"):
                    db.storage.delete(filepath)
                else:
                    os.remove(filepath)

    def on_delete(self, db: DatabaseInterface, key: str) -> None:
        if db.storage.filesystem:
            filepath = db.databases["data"][key]["content"]
            if isinstance(filepath, str):
                if filepath.startswith("pickle://"):
                    filepath = filepath[9:]
                elif filepath.startswith("bytes://"):
                    filepath = filepath[8:]
                elif filepath.startswith("text://"):
                    filepath = filepath[7:]
                else:
                    return
                if hasattr(db.storage, "delete"):
                    db.storage.delete(filepath)
                else:
                    os.remove(filepath)

    def pickle_encode(self, data: Any) -> bytes:
        return pickle.dumps(data)

    def pickle_decode(self, data: bytes) -> Any:
        return pickle.loads(data)

    def read(self, path: str) -> bytes:
        with open(path, "rb") as f:
            ret = f.read()
        return ret

    def write(self, path: str, data: bytes) -> None:
        with open(path, "wb") as f:
            f.write(data)
