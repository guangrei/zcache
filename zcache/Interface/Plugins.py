# -*-coding:utf8;-*-
from abc import ABC, abstractmethod


class Plugins(ABC):

    @abstractmethod
    def on_write(db, key, value):
        """
        trigger at Database.__set()
        return will affect on data content before write.
        """
        pass

    @abstractmethod
    def on_read(db, key, value):
        """
        trigger at Database.get()
        return will affect on data content after read.
        """
        pass

    @abstractmethod
    def on_limit(db, key, value, ttl):
        """
        trigger when Database limit reached on Database.set()
        return will not affect anything.
        """
        pass

    @abstractmethod
    def on_expired(db, key):
        """
        trigger when Database key time to live limit reached.
        return will not affect anything.
        """
        pass

    @abstractmethod
    def on_delete(db, key):
        """
        trigger on Database.delete()
        return will not affect anything.
        """
        pass
