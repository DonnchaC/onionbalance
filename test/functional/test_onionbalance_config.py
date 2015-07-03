# -*- coding: utf-8 -*-
"""
Functional tests which run the onionbalance-config tool and check
the created output files.
"""
import sys

import pexpect
import Crypto.PublicKey.RSA

import onionbalance.util


def onionbalance_config_interact(cli, cli_input):
    """
    Send each input line to the onionbalance-config CLI interface
    """
    cli.expect(u"store generated config")
    cli.send("{}\n".format(cli_input.get('config_dir', u'')))

    cli.expect(u"path to master service private key")
    cli.send(u"{}\n".format(cli_input.get('private_key_path', u'')))

    cli.expect(u"Number of instance services")
    cli.send(u"{}\n".format(cli_input.get('num_instances', u'')))

    cli.expect(u"Provide a tag name")
    cli.send(u"{}\n".format(cli_input.get('tag_name', u'')))

    cli.expect(u"service virtual port")
    cli.send(u"{}\n".format(cli_input.get('virtual_port', u'')))

    cli.expect(u"service target IP and port")
    cli.send(u"{}\n".format(cli_input.get('target_ip', u'')))

    cli.expect(u"optional password")
    cli.send(u"{}\n".format(cli_input.get('password', u'')))

    return None


def check_basic_config_output(config_dir):
    """
    Run basic tests on the generated config files and keys to check
    that they look reasonable.
    """

    assert len(config_dir.listdir()) == 1 + 2

    # Find generated instance addresses
    instance_addresses = []
    for directory in config_dir.listdir():
        if directory.basename != 'master':
            instance_addresses.extend(
                [str(name.basename) for name in directory.listdir()
                 if 'torrc' not in name.basename])

    # Correct number of directories created
    assert len(config_dir.listdir()) == 1 + 2

    assert config_dir.join('master', 'torrc-server').check()
    assert config_dir.join('master', 'config.yaml').check()

    config_file = config_dir.join('master', 'config.yaml').read_text('utf-8')
    assert all(address in config_file for address in instance_addresses)

    return True


def test_onionbalance_config_interactive(tmpdir):
    """
    Functional test to run onion-balance config in interactive mode.
    """
    # Start onionbalance-config in interactive mode (no command line arguments)
    cli = pexpect.spawnu("onionbalance-config", logfile=sys.stdout)
    cli.expect(u"entering interactive mode")

    # Interact with the running onionbalance-config process
    onionbalance_config_interact(
        cli, cli_input={'config_dir': str(tmpdir.join(u"configdir"))})
    cli.expect(u"Done! Successfully generated")

    check_basic_config_output(tmpdir.join(u"configdir"))


def test_onionbalance_config_automatic(tmpdir):
    """
    Functional test to run onion-balance config in automatic mode.
    """
    # Start onionbalance-config in automatic mode
    cli = pexpect.spawnu("onionbalance-config", logfile=sys.stdout,
                         args=[
                             '--output', str(tmpdir.join(u"configdir")),
                         ])
    cli.expect(u"Done! Successfully generated")

    check_basic_config_output(tmpdir.join(u"configdir"))


def test_onionbalance_config_automatic_custom_ports(tmpdir):
    """
    Run onionbalance-config in interactive mode, providing a custom port line.
    """
    cli = pexpect.spawnu("onionbalance-config", logfile=sys.stdout,
                         args=[
                             '--output', str(tmpdir.join(u"configdir")),
                             '--service-virtual-port', u'443',
                             '--service-target', u'127.0.0.1:8443',
                         ])
    cli.expect(u"Done! Successfully generated")

    # Read one of the generated torrc files
    for directory in tmpdir.join(u"configdir").listdir():
        if directory.basename != 'master':
            torrc_file = [name for name in directory.listdir()
                          if name.basename == 'instance_torrc'][0]
            break
    assert torrc_file.check()

    # Check torrc line contains the correct HiddenServicePort line
    torrc_contents = torrc_file.read_text('utf-8')
    assert u'HiddenServicePort 443 127.0.0.1:8443' in torrc_contents


def test_onionbalance_config_automatic_key_with_password(tmpdir, mocker):
    """
    Run onionbalance-config with an existing key, export as password protected
    key.
    """

    # Create input private_key
    private_key = Crypto.PublicKey.RSA.generate(1024)
    key_path = tmpdir.join('private_key')
    key_path.write(private_key.exportKey())

    # Start onionbalance-config in automatic mode
    cli = pexpect.spawnu("onionbalance-config", logfile=sys.stdout,
                         args=[
                             '--output', str(tmpdir.join(u"configdir")),
                             '--key', str(key_path),
                             '--password', 'testpassword',
                         ])
    cli.expect(u"Done! Successfully generated")

    # Check master config was generated with password protected key.
    master_dir = tmpdir.join('configdir', 'master')
    output_key_path = [fpath for fpath in master_dir.listdir()
                       if fpath.ext == '.key'][0]
    assert output_key_path.check()

    # Check key decrypts and is valid
    mocker.patch('getpass.getpass', lambda *_: 'testpassword')
    output_key = onionbalance.util.key_decrypt_prompt(str(output_key_path))
    assert isinstance(output_key, Crypto.PublicKey.RSA._RSAobj)
