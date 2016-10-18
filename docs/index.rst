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

- Load balancing between up to 60 backend hidden services
- Storage of the hidden service private key separate to the hidden service
  hosts


Quickstart
==========

Assuming there is no previous configuration in ``/etc/onionbalance``:

.. code-block:: console

   $ onionbalance-config
   $ sudo cp ./config/master/*.key /etc/onionbalance/
   $ sudo cp ./config/master/config.yaml /etc/onionbalance/
   $ sudo chown onionbalance:onionbalance /etc/onionbalance/*.key

Restart OnionBalance to reload the configuration files.

.. code-block:: console

   $ sudo service onionbalance restart

Check the logs. The following warnings are expected:
"Error generating descriptor: No introduction points for service ..."

.. code-block:: console

   $ sudo tail -f /var/log/onionbalance/log

Copy the ``instance_torrc`` and ``private_key`` files from each of the directories named ``./config/``, ``srv1``, ``srv2``, ... to each of the Tor servers providing the Onion Services.


User Guide
==========

OnionBalance consists of a long-running daemon and a command-line
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
   contributors
   changelog
