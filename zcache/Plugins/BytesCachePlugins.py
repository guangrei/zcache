# -*-coding:utf8;-*-
from zcache.Interface.Plugins import Plugins
import pickle
import os

"""
this plugins is good for large cache
author: guangrei
"""


class BytesCachePlugins(Plugins):

    useRandomName = True

    def on_write(db, key, value):  # noqa
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
                        BytesCachePlugins.write(filepath, value)
                    return "bytes://" + filepath
                elif isinstance(value, str):
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, value.encode("utf-8"))
                    else:
                        BytesCachePlugins.write(filepath, value.encode("utf-8"))
                    return "text://" + filepath
                else:
                    if hasattr(db.storage, "write"):
                        db.storage.write(
                            filepath, BytesCachePlugins.pickle_encode(value)
                        )
                    else:
                        BytesCachePlugins.write(
                            filepath, BytesCachePlugins.pickle_encode(value)
                        )
                    return "pickle://" + filepath
            else:
                if BytesCachePlugins.useRandomName:
                    import uuid

                    filename = ".zcache-" + uuid.uuid4().hex
                else:
                    filename = ".zcache-" + key
                filepath = os.path.join(path, filename)
                if isinstance(value, bytes):
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, value)
                    else:
                        BytesCachePlugins.write(filepath, value)
                    return "bytes://" + filepath
                elif isinstance(value, str):
                    if hasattr(db.storage, "write"):
                        db.storage.write(filepath, value.encode("utf-8"))
                    else:
                        BytesCachePlugins.write(filepath, value.encode("utf-8"))
                    return "text://" + filepath
                else:
                    if hasattr(db.storage, "write"):
                        db.storage.write(
                            filepath, BytesCachePlugins.pickle_encode(value)
                        )
                    else:
                        BytesCachePlugins.write(
                            filepath, BytesCachePlugins.pickle_encode(value)
                        )
                    return "pickle://" + filepath
        else:
            return value

    def on_read(db, key, value):
        if db.storage.filesystem:
            if isinstance(value, str):
                filepath = value
                if filepath.startswith("pickle://"):
                    if hasattr(db.storage, "read"):
                        ret = db.storage.read(filepath[9:])
                    else:
                        ret = BytesCachePlugins.read(filepath[9:])
                    return BytesCachePlugins.pickle_decode(ret)
                elif filepath.startswith("text://"):
                    if hasattr(db.storage, "read"):
                        ret = db.storage.read(filepath[7:])
                    else:
                        ret = BytesCachePlugins.read(filepath[7:])
                    return ret.decode("utf-8")
                elif filepath.startswith("bytes://"):
                    if hasattr(db.storage, "read"):
                        return db.storage.read(filepath[8:])
                    else:
                        return BytesCachePlugins.read(filepath[8:])
                else:
                    return value
            else:
                return value
        else:
            return value

    def on_limit():
        pass

    def on_expired(db, key):
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

    def on_delete(db, key):
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

    def pickle_encode(data):
        return pickle.dumps(data)

    def pickle_decode(data):
        return pickle.loads(data)

    def read(path):
        with open(path, "rb") as f:
            ret = f.read()
        return ret

    def write(path, data):
        with open(path, "wb") as f:
            f.write(data)
