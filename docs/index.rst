.. onionbalance documentation master file, created by
   sphinx-quickstart on Wed Jun 10 13:54:42 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
========

The OnionBalance software allows for Tor hidden service requests to be
distributed across multiple backend Tor instances. OnionBalance provides
load-balancing while also making onion services more resilient and reliable
by eliminating single points-of-failure.

- Latest release: |version| (:ref:`changelog`)
- GitHub: https://github.com/DonnchaC/onionbalance/
- Issue tracker: https://github.com/DonnchaC/onionbalance/issues
- PyPI: https://pypi.python.org/pypi/OnionBalance
- IRC: #onionbalance @ OFTC

Features
========

OnionBalance is under active development and new features are being added
regularly:

- Load balancing between up to 10 backend hidden services
- Storage of the hidden service private key separate to th hidden service
  hosts


User Guide
==========

Onionbalance consists of a long-running daemon and a command-line
configuration tool. Please see the :ref:`getting_started` page for usage
instructions.


.. toctree::
   :maxdepth: 2

   installation
   getting-started
   running-onionbalance
   use-cases

.. toctree::
   :maxdepth: 2

   design
   changelog
