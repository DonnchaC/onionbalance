Running OnionBalance
====================

Description
-----------

You can start the OnionBalance management server once all of your backend
onion service instances are running.

You will need to create a :ref:`configuration file <configuration_file_format>`
which list the backend hidden services and the location of your hidden
service keys.

.. code-block:: console

    $ onionbalance -c config.yaml

or

.. code-block:: console

    $ sudo service onionbalance start

The management server must be left running to publish new descriptors for
your onion service.

.. note::

    Multiple OnionBalance management servers can be run simultaneously with
    the same master private key and configuration file to provide redundancy.

Command-Line Options
--------------------

.. autoprogram:: onionbalance.manager:parse_cmd_args()
   :prog: onionbalance


.. _configuration_file_format:

Configuration File Format
-------------------------

The OnionBalance management server is primarily configured using a YAML
configuration file.

.. literalinclude:: ../onionbalance/data/config.example.yaml
   :name: example-config.yaml
   :language: yaml


The ``services`` section of the configuration file contains a list of
master onion services that OnionBalance is responsible for.

Each ``key`` option specifies the location of the 1024 bit private RSA key
for the hidden service. This master private key determines the address
that users will use to access your onion service. This private key **must**
be kept secure.

The location of the private key is evaluated as an absolute path, or
relative to the configuration file location.

You can use existing Tor hidden service private key with OnionBalance
to keep your onion address.

Each backend Tor onion service instance is listed by its unique onion
address in the ``instances`` list.

.. note::

    You can replace backend instance keys if they get lost or compromised.
    Simply start a new backend hidden service under a new key and replace
    the ``address`` in the config file.

If you have used the :ref:`onionbalance-config <onionbalance_config>` tool
you can simply use the generated config file from ``master/config.yaml``.

.. note::

    By default onionbalance will search for a ``config.yaml`` file in
    the current working directory.


Configuration Options
~~~~~~~~~~~~~~~~~~~~~

The OnionBalance command line options can also be specified in the
OnionBalance configuration file. Options specified on the command line
take precedence over the related configuration file options:

TOR_CONTROL_SOCKET:
  The location of the Tor unix domain control socket. OnionBalance will
  attempt to connect to this control socket first before falling back to
  using a control port connection.
  (default: /var/run/tor/control)

TOR_ADDRESS:
  The address where the Tor control port is listening. (default: 127.0.0.1)

TOR_PORT:
  The Tor control port. (default: 9051)

TOR_CONTROL_PASSWORD:
  The password for authenticating to a Tor control port which is using the
  HashedControlPassword authentication method. This is not needed when the
  Tor control port is using the more common CookieAuthentication method.
  (default: None)

Other options:

LOG_LOCATION
  The path where OnionBalance should write its log file.

LOG_LEVEL
  Specify the minimum verbosity of log messages to output. All log messages
  equal or higher the the specified log level are output. The available
  log levels are the same as the --verbosity command line option.

REFRESH_INTERVAL
  How often to check for updated backend hidden service descriptors. This
  value can be increased if your backend instance are under heavy loaded
  causing them to rotate introduction points quickly.
  (default: 600 seconds).

PUBLISH_CHECK_INTERVAL
  How often should to check if new descriptors need to be published for
  the master hidden service (default: 360 seconds).

INITIAL_DELAY
  How long to wait between starting OnionBalance and publishing the master
  descriptor. If you have more than 20 backend instances you may need to wait
  longer for all instance descriptors to download before starting
  (default: 45 seconds).

DISTINCT_DESCRIPTORS
  Distinct descriptors are used if you have more than 10 backend instances.
  At the cost of scalability, this can be disabled to appear more like a
  standard onion service. (default: True)

STATUS_SOCKET_LOCATION
  The OnionBalance service creates a Unix domain socket which provides
  real-time information about the currently loaded service and descriptors.
  This option can be used to change the location of this domain socket.
  (default: /var/run/onionbalance/control)

The following options typically do not need to be modified by the end user:

REPLICAS
  How many set of HSDirs to upload too (default: 2).

MAX_INTRO_POINTS
  How many introduction points to include in a descriptor (default: 10)

DESCRIPTOR_VALIDITY_PERIOD
  How long a hidden service descriptor remains valid (default:
  86400 seconds)

DESCRIPTOR_OVERLAP_PERIOD
  How long to overlap hidden service descriptors when changing
  descriptor IDs (default: 3600 seconds)

DESCRIPTOR_UPLOAD_PERIOD
  How often to publish a descriptor, even when the introduction points
  don't change (default: 3600 seconds)


Environment Variables
~~~~~~~~~~~~~~~~~~~~~

ONIONBALANCE_CONFIG
  Override the location for the OnionBalance configuration file.

The loaded configuration file takes precedence over environment variables.
Configuration file options will override environment variable which have the
same name.

ONIONBALANCE_LOG_LOCATION
  See the config file option.

ONIONBALANCE_LOG_LEVEL
  See the config file option

ONIONBALANCE_STATUS_SOCKET_LOCATION
  See the config file option

ONIONBALANCE_TOR_CONTROL_SOCKET
  See the config file option


Files
-----

/etc/onionbalance/config.yaml
  The configuration file, which contains ``services`` entries.

config.yaml
  Fallback location for torrc, if /etc/onionbalance/config.yaml is
  not found.

See Also
--------

Full documentation for the **OnionBalance** software is available at
https://onionbalance.readthedocs.org/
