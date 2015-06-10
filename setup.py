# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import onionbalance

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name = "OnionBalance",
    packages = ["onionbalance"],
    entry_points = {
        "console_scripts": ['onionbalance = onionbalance.manager:main']
        },
    description = "Tool for distributing Tor onion services connections to "
                  "multiple backend Tor instances",
    long_description = long_descr,
    version = onionbalance.__version__,
    author = onionbalance.__author__,
    author_email = onionbalance.__contact__,
    url = onionbalance.__url__,
    license = onionbalance.__license__,
    keywords = 'tor',
    install_requires = [
        'stem>=1.3.0-dev',
        'PyYAML>=3.11',
        'pycrypto>=2.6.1',
        'schedule>=0.3.1',
        ],
    tests_require = ['tox'],
    cmdclass = {'test': Tox},
)
