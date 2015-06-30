# -*- coding: utf-8 -*-
import os
import sys
import socket
import time

import pytest
import Crypto.PublicKey.RSA
import yaml
import pexpect
import stem.control

import onionbalance.util

# Skip functional tests if Chutney environment is not running.
pytestmark = pytest.mark.skipif(
    "os.environ.get('CHUTNEY_ONION_ADDRESS') is None",
    reason="Skipping functional test, no Chutney environment detected")


def parse_chutney_enviroment():
    """
    Read environment variables and determine chutney instance and
    client addresses.
    """

    tor_client = os.environ.get('CHUTNEY_CLIENT_PORT')
    assert tor_client

    # Calculate the address and port of clients control port
    client_address, client_socks_port = tor_client.split(':')
    client_ip = socket.gethostbyname(client_address)

    tor_client_number = int(client_socks_port) - 9000
    # Control port in the 8000-8999 range, offset by Tor client number
    control_port = 8000 + tor_client_number
    assert control_port

    # Retrieve instance onion address exported during chutney setup
    instance_address = os.environ.get('CHUTNEY_ONION_ADDRESS')
    assert instance_address  # Need at least 1 instance address for test

    if '.onion' in instance_address:
        instance_address = instance_address[:16]

    return {
        'client_ip': client_ip,
        'control_port': control_port,
        'instances': [instance_address],
    }


def create_test_config_file(tmppath, private_key=None, instances=None):
    """
    Setup function to create a temp directory with master key and config file.
    Returns a path to the temporary config file.

    .. todo:: Refactor settings.py config creation to avoid code duplication
              in integration tests.
    """

    if not private_key:
        private_key = Crypto.PublicKey.RSA.generate(1024)

    # Write private key file
    key_path = tmppath.join('private_key')
    key_path.write(private_key.exportKey())
    assert key_path.check()

    # Create YAML OnionBalance settings file for these instances
    service_data = {'key': str(key_path)}
    service_data['instances'] = [{'address': addr} for addr in instances]
    settings_data = {'services': [service_data]}
    config_yaml = yaml.dump(settings_data, default_flow_style=False)

    config_path = tmppath.join('config.yaml')
    config_path.write_binary(config_yaml.encode('utf-8'))
    assert config_path.check()

    return str(config_path)


def test_master_descriptor_publication(tmpdir):
    """
    Functional test to run OnionBalance, publish a master descriptor and
    check that it can be retrieved from the DHT.
    """

    chutney_config = parse_chutney_enviroment()
    private_key = Crypto.PublicKey.RSA.generate(1024)
    master_onion_address = onionbalance.util.calc_onion_address(private_key)

    config_file_path = create_test_config_file(
        tmppath=tmpdir,
        private_key=private_key,
        instances=chutney_config.get('instances', []),
    )
    assert config_file_path

    # Start an OnionBalance server and monitor for correct output with pexpect
    server = pexpect.spawnu("onionbalance",
                            args=[
                                '-i', chutney_config.get('client_ip'),
                                '-p', str(chutney_config.get('control_port')),
                                '-c', config_file_path,
                                '-v', 'debug',
                            ], logfile=sys.stdout, timeout=15)

    # Check for expected output from OnionBalance
    server.expect(u"Loaded the config file")
    server.expect(u"introduction point set has changed")
    server.expect(u"Published a descriptor", timeout=120)

    # Check Tor control port gave an uploaded event.

    server.expect(u"HS_DESC UPLOADED")
    # Eek, sleep to wait for descriptor upload to all replicas to finish
    time.sleep(10)

    # .. todo:: Also need to check and raise for any warnings or errors
    #           that are emitted

    # Try fetch and validate the descriptor with stem
    with stem.control.Controller.from_port(
        address=chutney_config.get('client_ip'),
        port=chutney_config.get('control_port')
    ) as controller:
        controller.authenticate()

        # get_hidden_service_descriptor() will raise exceptions if it
        # cannot find the descriptors
        master_descriptor = controller.get_hidden_service_descriptor(
            master_onion_address)
        master_ips = master_descriptor.introduction_points()

        # Try retrieve a descriptor for each instance
        for instance_address in chutney_config.get('instances'):
            instance_descriptor = controller.get_hidden_service_descriptor(
                instance_address)
            instance_ips = instance_descriptor.introduction_points()

            # Check if all instance IPs were included in the master descriptor
            assert (set(ip.identifier for ip in instance_ips) ==
                    set(ip.identifier for ip in master_ips))
