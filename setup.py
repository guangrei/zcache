#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

requirements = ["types-aiofiles", "aiohttp", "aiofiles"]

setup(
    name="zcache",
    version="v3.0.3",
    packages=find_packages(),
    license="MIT",
    author="guangrei",
    author_email="myawn@pm.me",
    description="Pure typed Python Key Value Database/Cache with abstract storage, plugins and asynchronous support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="cache key value file json",
    url="https://github.com/guangrei/zcache",
    install_requires=requirements,
)
