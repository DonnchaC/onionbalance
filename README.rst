.. WARNING ::
    THIS IS VERY EXPERIMENTAL, ROUGH CODE. THIS IS NOT READY TO BE
    USED FOR PRODUCTION. IT MAY CONTAIN CRITICAL SECURITY OR PERFORMANCE
    BUGS.

Overview
--------

The OnionBalance software allows the distribution of requests for an onion service to between 1 and 10 separate Tor instances. Each Tor instance can run
independently with no knowledge of the other instances.

* `Documentation <https://onionbalance.readthedocs.org>`_
* `Code <https://github.com/DonnchaC/onionbalance/>`_
* `Bug Tracker <https://github.com/DonnchaC/onionbalance/issues>`_

|build-status| |docs|

Installation
------------

Onion Service Instances
~~~~~~~~~~~~~~~~~~~~~~~~

Each load-balancing instance is an onion service configured with a
unique private key. To minimize the disclosure of information about your
onion service configuration it is advisable to configure some form of
onion service authentication.

The individual load balancing instances use a standard Tor client.

Management Server
~~~~~~~~~~~~~~~~~

Generate a key for your onion service.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use your existing onion service ``private_key`` or generate a
new one using OpenSSL.

::

    $ openssl genrsa -out private_key 1024

Encrypt an onion service private key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your master onion service private key can be protected by encrypting it
while it is stored on disk. Due to limitation in the underlying pycrypto
library, only DES-CBC, DES-EDE3-CBC, AES-128-CBC encrypted keys are
supported.

::

    $ openssl rsa -des3 -in private_key -out private_key.enc

Configure Tor on the management server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The management server must run a release of Tor >= 0.2.7.1-alpha. Tor can be installed from the Tor repositions or compiled from source code.

The ``data/torrc-server`` contains a sample Tor config file which is suitable
for the management server.

Install the management server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The management server code is available from the project's Git repository.

::

    $ git clone https://github.com/DonnchaC/onionbalance.git
    $ cd onionbalance

The server can be install in a virtual environment or system-wide with the included setup script.
::

    $ sudo python setup.py install

Configuration
-------------

Each load balancing Tor instance is listed by it's unique onion address. An example config file is provided in ``config.yaml.example``.

Running
-------

Once your load balancing instances are running, you can start the management server which will begin publishing master descriptors:

::

    $ onionbalance -c config.yaml

.. |build-status| image:: https://img.shields.io/travis/DonnchaC/onionbalance.svg?style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/DonnchaC/onionbalance

.. |docs| image:: https://readthedocs.org/projects/onionbalance/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://onionbalance.readthedocs.org/en/latest/
