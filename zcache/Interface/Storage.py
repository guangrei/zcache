# -*-coding:utf8;-*-
from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, path):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, data):
        pass
