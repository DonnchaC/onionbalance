# -*- coding: utf-8 -*-

"""
Implements the generation and loading of configuration files.
"""

import os
import sys

import yaml

from onionbalance import config
from onionbalance import util
from onionbalance import log

import onionbalance.service
import onionbalance.instance

logger = log.get_logger()


def parse_config_file(config_file):
    """
    Parse config file containing service information
    """
    config_path = os.path.abspath(config_file)
    if os.path.exists(config_path):
        with open(config_file, 'r') as handle:
            config_data = yaml.load(handle.read())
            logger.info("Loaded the config file '%s'.", config_path)
    else:
        logger.error("The specified config file '%s' does not exist.",
                     config_path)
        sys.exit(1)

    return config_data


def initialize_services(controller, services_config):
    """
    Load keys for services listed in the config
    """

    # Load the keys and config for each onion service
    for service in services_config:
        service_key = util.key_decrypt_prompt(service.get("key"))
        if not service_key:
            logger.error("Private key %s could not be loaded.",
                         service.get("key"))
            sys.exit(0)
        else:
            # Successfully imported the private key
            onion_address = util.calc_onion_address(service_key)
            logger.debug("Loaded private key for service %s.onion.",
                         onion_address)

        # Load all instances for the current onion service
        instance_config = service.get("instances", [])
        if not instance_config:
            logger.error("Could not load and instances for service "
                         "%s.onion.", onion_address)
            sys.exit(1)
        else:
            instances = []
            for instance in instance_config:
                instances.append(onionbalance.instance.Instance(
                    controller=controller,
                    onion_address=instance.get("address"),
                    authentication_cookie=instance.get("auth")
                ))

            logger.info("Loaded %d instances for service %s.onion.",
                        len(instances), onion_address)

        # Store service configuration in config.services global
        config.services.append(onionbalance.service.Service(
            controller=controller,
            service_key=service_key,
            instances=instances
        ))


def generate_config():
    """
    Entry point for interactive config file generation.
    """
    return None
    logger.info("Config generation")
