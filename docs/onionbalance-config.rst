.. _onionbalance_config:

onionbalance-config Tool
========================

Description
-----------

The ``onionbalance-config`` tool is the fastest way to generate the necessary
keys and config files to get your onion service up and running.

.. code-block:: console

    $ onionbalance-config

When called without any arguments, the config generator will run in an
interactive mode and prompt for user input.

The ``master`` directory should be stored on the management server while
the other ``instance`` directories should be transferred to the respective
backend servers.


Command-Line Options
--------------------

.. autoprogram:: onionbalance.manager:parse_cmd_args()
   :prog: onionbalance-config


Files
-----

master/config.yaml
  This is the configuration file that is used my the OnionBalance management
  server.

master/<ONION_ADDRESS>.key
  The private key which will become the public address and identity for your
  hidden service. It is essential that you keep this key secure.

master/torrc-server
  A sample Tor configuration file which can be used with the Tor instance
  running on the management server.

srv/torrc-instance
  A sample Tor config file which contains the Tor ``HiddenService*`` options
  needed for your backend Tor instance.

srv/<ONION_ADDRESS>/private_key
  Directory containing the private key for you backend hidden service instance.
  This key is less critical as it can be rotated if lost or compromised.


See Also
--------

Full documentation for the **OnionBalance** software is available at
https://onionbalance.readthedocs.org/
