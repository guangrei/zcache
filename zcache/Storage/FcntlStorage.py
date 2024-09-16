# -*-coding:utf8;-*-
import zcache
from zcache.Interface.Storage import Storage
import time
import json
import fcntl
import os


class FileLock:
    def __init__(self, filename):
        self.filename = filename
        self.file_handle = None

    def __enter__(self):
        self.file_handle = open(self.filename, "a+")
        fcntl.flock(self.file_handle, fcntl.LOCK_EX)
        return self.file_handle

    def __exit__(self, exc_type, exc_value, traceback):
        fcntl.flock(self.file_handle, fcntl.LOCK_UN)
        self.file_handle.close()


class FcntlStorage(Storage):

    filesystem = True

    def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError
        if not os.path.exists(path):
            self.create(path)
        self.path = path

    def create(self, path):
        data = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = zcache.__version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        with FileLock(path) as f:
            f.write(json.dumps(data))

    def load(self):
        with FileLock(self.path) as f:
            return json.loads(f.read())

    def save(self, data):
        data = json.dumps(data)
        with FileLock(self.path) as f:
            f.write(data)
