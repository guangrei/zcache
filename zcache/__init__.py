# -*-coding:utf8;-*-
from .Core.Database import Database
from .Core.AsyncDatabase import AsyncDatabase


Cache = Database
AsyncCache = AsyncDatabase
__version__ = "3.0.4"
__author__ = "Guangrei <myawn@pm.me>"
__license__ = "MIT"
