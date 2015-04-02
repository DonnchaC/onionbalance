# -*- coding: utf-8 -*-
class Config(object):
    """
    Config object to store the global state
    """
    def __init__(self):
        # Configure some defaults
        self.config = {
            'replicas': 2,
            'max_intro_points': 10,
            'refresh': 10 * 60
        }
        # In memory list of hidden services and balancing instances
        self.hidden_services = []

cfg = Config()
