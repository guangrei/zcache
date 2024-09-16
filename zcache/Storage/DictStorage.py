# -*-coding:utf8;-*-
import zcache
from zcache.Interface.Storage import Storage
import time


class DictStorage(Storage):
    database = {}
    filesystem = False

    def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError
        if path not in self.database:
            self.create(path)
        self.path = path

    def create(self, path):
        data = {}
        data["first_created"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["version"] = zcache.__version__
        data["url"] = "https://github.com/guangrei/zcache"
        data["data"] = {}
        data["limit"] = 0
        self.database[path] = data

    def load(self):
        return self.database[self.path]

    def save(self, data):
        self.database[self.path] = data
