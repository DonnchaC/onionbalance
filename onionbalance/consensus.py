# -*- coding: utf-8 -*-
"""
This module provides a set of functions for reading Tor consensus documents.
"""
from bisect import bisect_left
import base64
import binascii

import stem
import stem.descriptor

import onionbalance.log as log
import onionbalance.config as config

logger = log.get_logger()

HSDIR_LIST = []


def refresh_consensus():
    """
    Update consensus state when Tor receives a new network status

    Retrieve the current set of hidden service directories
    """
    global HSDIR_LIST

    if not config.controller:
        logger.warning("Controller connection not found in the configuration. "
                       "Cannot update the Tor state.")
        return None
    else:
        controller = config.controller

    # pylint: disable=no-member
    # Retrieve the current set of hidden service directories
    hsdirs = []
    try:
        for desc in controller.get_network_statuses():
            if stem.Flag.HSDIR in desc.flags:
                hsdirs.append(desc.fingerprint)
    except IOError as err:
        logger.error("Could not load consensus from Tor: %s" % err)
    else:
        HSDIR_LIST = hsdirs
        logger.debug("Updated the list of Tor hidden service directories.")


def get_hsdirs(descriptor_id):
    """
    Get the responsible HSDirs for a given descriptor ID.
    """

    # Try fetch a consensus if we haven't loaded one already
    if not HSDIR_LIST:
        refresh_consensus()

    if not HSDIR_LIST:
        raise ValueError('Could not determine the responsible HSDirs.')

    desc_id_bytes = base64.b32decode(descriptor_id, 1)
    descriptor_id_hex = (binascii.hexlify(desc_id_bytes).
                         decode('utf-8').upper())

    responsible_hsdirs = []

    # Find postion of descriptor ID in the HSDir list
    index = descriptor_position = bisect_left(HSDIR_LIST, descriptor_id_hex)

    # Pick HSDirs until we have enough
    while len(responsible_hsdirs) < config.HSDIR_SET:
        try:
            responsible_hsdirs.append(HSDIR_LIST[index])
            index += 1
        except IndexError:
            # Wrap around when we reach the end of the HSDir list
            index = 0

        # Do not choose a HSDir more than once
        if index == descriptor_position:
            break

    return responsible_hsdirs
