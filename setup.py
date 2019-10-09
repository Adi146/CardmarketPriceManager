#!/usr/bin/env python
from setuptools import setup

setup(
    name="CardmarketPriceManager",
    version="1.0",
    description="Price Manager for cardmarket.com",
    author="Adi146",
    author_email="adihuber12@gmail.com",
    packages=["CardMarketPriceManager"],
    install_requires=["mkmsdk", "pyyaml"],
)
