# -*-coding:utf8;-*-
import zcache
from zcache.Interface.Storage import Storage
import time
import json
import os


class BaseFileStorage(Storage):

    filesystem = True

    def __init__(self, path):
        if not isinstance(path, str):
            raise TypeError
        if os.path.isdir(path):
            path = os.path.join(path, "zcache.json")
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
        with open(path, "w") as f:
            f.write(json.dumps(data))

    def load(self):
        with open(self.path, "r") as f:
            return json.loads(f.read())

    def save(self, data):
        data = json.dumps(data)
        with open(self.path, "w") as f:
            f.write(data)
