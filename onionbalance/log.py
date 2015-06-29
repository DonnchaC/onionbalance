# -*- coding: utf-8 -*-
import logging

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt="%(asctime)s [%(levelname)s]: "
                                           "%(message)s"))

logger = logging.getLogger("onionbalance")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def get_logger():
    """
    Returns a logger.
    """
    return logger


def get_config_generator_logger():
    """
    Simplified logger for interactive config generator CLI
    """
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt="[%(levelname)s]: "
                                               "%(message)s"))

    logger = logging.getLogger("onionbalance-config")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
