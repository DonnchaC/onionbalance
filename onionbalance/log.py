# -*- coding: utf-8 -*-
import logging
import logging.handlers

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


def setup_file_logger(log_file):
    """
    Add log file handler to the existing logger
    """
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=3)
    handler.setFormatter(logging.Formatter(fmt="%(asctime)s [%(levelname)s]: "
                                           "%(message)s"))
    logging.getLogger('onionbalance').addHandler(handler)


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
