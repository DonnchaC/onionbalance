OnionBalance
============

Introduction
------------

The OnionBalance software allows for Tor hidden service requests to be distributed across multiple backend Tor instances. OnionBalance provides load-balancing while also making onion services more resilient and reliable by eliminating single points-of-failure.

* `Documentation <https://onionbalance.readthedocs.org>`_
* `Code <https://github.com/DonnchaC/onionbalance/>`_
* `Bug Tracker <https://github.com/DonnchaC/onionbalance/issues>`_

|build-status| |docs|

Getting Started
---------------

OnionBalance requires a system which runs the OnionBalance management server and up to 10 backend servers which run onion services that serve the desired content (web site, IRC server etc.).

Installing OnionBalance
~~~~~~~~~~~~~~~~~~~~~~~

::

    $ pip install onionbalance

or

::

    $ git clone https://github.com/DonnchaC/onionbalance.git
    $ cd onionbalance
    $ python setup.py install

The management server does not need to be installed on the same systems that host the backend onion service instances.


Configuring the OnionBalance management server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bundled ``onionbalance-config`` tool is the fastest way to generate the necessary keys and config files to get your onion service up and running.

::

    $ onionbalance-config

The config generator runs in an interactive mode when called without any arguments. The ``master`` directory should be stored on the management server while the other instance directories should be transferred to the respective backend servers.


Configuring Tor on the management server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OnionBalance requires that a recent version of Tor (>= 0.2.7.1-alpha) is installed on the management server system. This versions of Tor is not yet available from the Tor repositories yet and must be compiled from source.

::

    $ wget https://www.torproject.org/dist/tor-0.2.7.1-alpha.tar.gz
    $ tar -xzvf tor-0.2.7.1-alpha.tar.gz && cd tor-0.2.7.1-alpha
    $ ./configure --disable-asciidoc && sudo make install

The Tor config file at ``onionbalance/data/torrc-server`` can be used for the management server. The ``onionbalance-config`` tool also outputs a suitable Tor config file as ``master/torrc-server``.

::

    $ tor -f torrc-server

Configuring the backend onion service instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each backend instance should be run a standard onion service which serves your website or other content. More information about configuring onion services is available in the Tor Project's `hidden service configuration guide <https://www.torproject.org/docs/tor-hidden-service.html.en>`_.

If you have used the ``onionbalance-config`` tool you should transfer the generated instance config files and keys to the respective backend servers. You can then start the onion service instance by simply running:

::

    $ tor -f instance_torrc

OnionBalance config file
~~~~~~~~~~~~~~~~~~~~~~~~

The OnionBalance management server must have access to the private key for the master onion service. This master private key determines the address that users will use to access your onion service. This private key must be kept secure.

The location of the private key must be specified as relative or absolute path under ``key`` in the config file. Each backend Tor onion service instance is listed by it's unique onion address in the ``instances`` list.

An example config file is provided in `config.example.yaml <onionbalance/data/config.example.yaml>`_. If you have used the ``onionbalance-config`` tool you can simply use the generated config file at ``master/config.yaml``.

Running
~~~~~~~


You can start the management server once your backend onion service instances are running. The management server must be left running to publish descriptors for your onion service.

::

    $ onionbalance -c config.yaml

Multiple OnionBalance management servers can be run to make your service more resilient and remove a single point of failure. Each redundant server should be run with the same private key and config file.

Use Cases
---------

- A popular onion service with an overloaded web server or Tor process

  A service such as Facebook which gets a large number of users would like to distribute client requests across multiple servers as the load is too much for a single Tor instance to handle. They would also like to balance between instances when the 'encrypted services' proposal is implemented [2555].

- Redundancy and automatic failover

  A political activist would like to keep their web service accessible and secure in the event that the secret police seize some of their servers. Clients should ideally automatically fail-over to another online instances with minimal service disruption.

- 'Shared Hosting' scenarios

  A hosting provider wishes to allow their customers to access their shared hosting control panel over an encrypted onion service. Rather than creating an individual onion service (with corresponding overhead) for thousands of customers, the host could instead run one onion service. Multiple service descriptors could then be published under unique customer onion addresses which would then be routed to that users control panel. This could also enable a low-resourced OnionFlare-type implementation.

- Secure Onion Service Key storage

  An onion service operator would like to compartmentalize their permanent onion key in a secure location separate to their Tor process and other services. With this proposal permanent keys could be stored on an independent, isolated system.

Contact
-------

This software is under active development and likely contains many bugs. Please open bugs on Github if you discover any issues with the software or documentation.

I can also be contacted by PGP email or on IRC at ``#onionbalance`` on the OFTC network.

::

    pub   4096R/0x3B0D706A7FBFED86 2013-06-27 [expires: 2016-07-11]
          Key fingerprint = 7EFB DDE8 FD21 11AE A7BE  1AA6 3B0D 706A 7FBF ED86
    uid                 [ultimate] Donncha O'Cearbhaill <donncha@donncha.is>
    sub   3072R/0xD60D64E73458F285 2013-06-27 [expires: 2016-07-11]
    sub   3072R/0x7D49FC2C759AA659 2013-06-27 [expires: 2016-07-11]
    sub   3072R/0x2C9C6F4ABBFCF7DD 2013-06-27 [expires: 2016-07-11]

.. |build-status| image:: https://img.shields.io/travis/DonnchaC/onionbalance.svg?style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/DonnchaC/onionbalance

.. |docs| image:: https://readthedocs.org/projects/onionbalance/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://onionbalance.readthedocs.org/en/latest/
