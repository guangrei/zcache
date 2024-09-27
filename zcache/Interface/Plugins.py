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
