# -*- coding: utf-8 -*-
import pytest

from onionbalance import consensus
from onionbalance import config

# Mock hex-encoded HSDir fingerprint list
MOCK_HSDIR_LIST = [
    "1111111111111111111111111111111111111111",
    "2222222222222222222222222222222222222222",
    "3333333333333333333333333333333333333333",
    "4444444444444444444444444444444444444444",
    "5555555555555555555555555555555555555555",
    "6666666666666666666666666666666666666666",
]

config.HSDIR_SET = 3  # Always select 3 responsible HSDirs


def test_get_hsdirs_no_consensus():
    """
    `get_hsdirs` should raise an exception when we don't have a valid
    HSDir list from the consensus.
    """

    with pytest.raises(ValueError):
        consensus.get_hsdirs('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')


def test_get_hsdirs(monkeypatch):
    """Test for normal responsible HSDir selection"""

    monkeypatch.setattr(consensus, 'HSDIR_LIST', MOCK_HSDIR_LIST)

    # Descriptor ID before '222....''
    descriptor_id_base32 = "eiqaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    responsible_hsdirs = consensus.get_hsdirs(descriptor_id_base32)

    assert (responsible_hsdirs == [
        "2222222222222222222222222222222222222222",
        "3333333333333333333333333333333333333333",
        "4444444444444444444444444444444444444444",
    ])


def test_get_hsdirs_edge_of_ring(monkeypatch):
    """Test that selection wraps around the edge of the HSDir ring"""

    monkeypatch.setattr(consensus, 'HSDIR_LIST', MOCK_HSDIR_LIST)

    # Descriptor ID before '666....''
    descriptor_id_base32 = "mzqaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    responsible_hsdirs = consensus.get_hsdirs(descriptor_id_base32)

    assert (responsible_hsdirs == [
        "6666666666666666666666666666666666666666",
        "1111111111111111111111111111111111111111",
        "2222222222222222222222222222222222222222",
    ])


def test_get_hsdirs_no_repeat(monkeypatch):
    """Test that selection wraps around the edge of the HSDir ring"""

    SHORT_HSDIR_LIST = [
        "1111111111111111111111111111111111111111",
        "2222222222222222222222222222222222222222",
    ]
    monkeypatch.setattr(consensus, 'HSDIR_LIST', SHORT_HSDIR_LIST)

    # Descriptor ID before '111....''
    descriptor_id_base32 = "ceiaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    responsible_hsdirs = consensus.get_hsdirs(descriptor_id_base32)

    assert (responsible_hsdirs == [
        "1111111111111111111111111111111111111111",
        "2222222222222222222222222222222222222222",
    ])
