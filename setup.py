#!/usr/bin/env python3
# https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
# TODO: This was unfinished, could be improved later

from setuptools import find_packages, setup

setup(
    name='lnb-node',
    version='0.1.0',
    description="Lightning Locator Node",
    author="Sean Duffie",
    url="https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html",
    packages=['node'],
    install_requires=[

    ],
    extras_require={
        
    }
)