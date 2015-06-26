# -*- coding: utf-8 -*-
import io
import os

import pytest

from onionbalance import settings
from .util import builtin

CONFIG_FILE_VALID = u'\n'.join([
    "services:",
    "    - key: private.key",
    "      instances:",
    "        - address: fqyw6ojo2voercr7",
    "        - address: facebookcorewwwi",
])

CONFIG_FILE_ABSOLUTE = u'\n'.join([
    "services:",
    "    - key: /absdir/private.key",
    "      instances:",
    "        - address: fqyw6ojo2voercr7",
    "        - address: facebookcorewwwi",
])


def test_parse_config_file_valid(mocker):
    # Patch config file read
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch(builtin('open'),
                 lambda *_: io.StringIO(CONFIG_FILE_VALID))

    parsed_config = settings.parse_config_file('/configdir/config_rel.yaml')

    assert len(parsed_config['services']) == 1
    assert len(parsed_config['services'][0]['instances']) == 2

    # Test key with absolute path
    assert os.path.dirname(parsed_config['services'][0]['key']) == '/configdir'

    # Test key with absolute path
    mocker.patch(builtin('open'),
                 lambda *_: io.StringIO(CONFIG_FILE_ABSOLUTE))
    parsed_config = settings.parse_config_file('/configdir/config_abs.yaml')
    assert os.path.dirname(parsed_config['services'][0]['key']) == '/absdir'


def test_parse_config_file_does_not_exist(mocker):
    with pytest.raises(SystemExit):
        settings.parse_config_file('doesnotexist/config.yaml')
