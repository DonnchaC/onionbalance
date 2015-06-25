# -*- coding: utf-8 -*-
from binascii import hexlify, unhexlify
import base64
import datetime
import io
import sys

import Crypto.PublicKey.RSA

import pytest
from .util import builtin

from onionbalance.util import *


PEM_PRIVATE_KEY = u'\n'.join([
    "-----BEGIN RSA PRIVATE KEY-----",
    "MIICWwIBAAKBgQDXzP6HGtjPSy7uF9OlY7ZmefTVKcFLsq0mSEzQrW5wSiNuYc+d",
    "oSV2OWxPg+1fVe19ES43AUkq/bS/gjAMLOunP6u9FbPDojyh1Vs/6TVqftS3sPkl",
    "Q0ItrrZwAwhtHC0WaEyrwYJNOSCBq3wpupdQhpRyWJFqMwm9+iBCG1QcJQIDAQAB",
    "AoGAegc2Sqm4vgdyozof+R8Ybnw6ISu6XRbNaJ9rqHjZwW9695khsK4GJAM2pwQf",
    "/0/0ukszyfDVMhVC1yREDS59lgzNecItd6nQZWbwr9TFxIoa9ouTqk8PcAoNixTb",
    "wafjPcMmWGakizXeAHiOfazPBH4x2keDQCulxfYxXZxTpyECQQDqZu61kd1S3U7T",
    "BT2NQBd3tHX0Hvonx+IkOKXwpHFY0Mo4d32Bi+MxRuEnd3tO44AaMvlkl13QMTF2",
    "kHFSC70dAkEA669LZavGjW67+rO+f+xyDVby9pD5GJQBb78xRCf93Zcu2KW4NSp3",
    "XC4p4eWfLgff1VuXL7g0VdFm4wUUHqYUqQJAZLmqpjdyBeO3tZIw6vu5meTgMvEE",
    "ygdos+vr0sa3NlUyMKWYNwznqgstQYpkYHf+WkPBS2qIE6iv+qUDLSCCOQJAESSk",
    "CFYxUBJQ7BBs9+Mb/Kppa9Ppuobxf85ZaAq8pYScrLeJKZzYJ8VX2I2aQX/jISLT",
    "YW41qFRd9n9lEkGkWQJAcxPmNI+2r5zJG+K148LLmWCIDTVZ4nxOcxffHka/3tCJ",
    "lDGUw4p2wU6pVRDpNfKrF5Nc9ZKO8NAtC17ZvDyVkQ==",
    "-----END RSA PRIVATE KEY-----",
])

PEM_INVALID_KEY = u'\n'.join([
    "-----BEGIN RSA PRIVATE KEY-----",
    "MIICWwIBAAKBgQDXzP6HGtjPSy7uF9OlY7ZmefTVKcFLsq0mSEzQrW5wSiNuYc+d",
    "oSV2OWxPg+1fVe19ES43AUkq/bS/gjAMLOunP6u9FbPDojyh1Vs/6TVqftS3sPkl",
    "Q0ItrrZwAwhtHC0WaEyrwYJNOSCBq3wpupdQhpRyWJFqMwm9+iBCG1QcJQIDAQAB",
    "AoGAegc2Sqm4vgdyozof+R8Ybnw6ISu6XRbNaJ9rqHjZwW9695khsK4GJAM2pwQf",
    "/0/0ukszyfDVMhVC1yREDS59lgzNecItd6nQZWbwr9TFxIoa9ouTqk8PcAoNixTb",
    "wafjPcMmWGakizXeAHiOfazPBH4x2keDQCulxfYxXZxTpyECQQDqZu61kd1S3U7T",
    "BT2NQBd3t          This is an invalid key             lkl13QMTF2",
    "kHFSC70dAkEA669LZavGjW67+rO+f+xyDVby9pD5GJQBb78xRCf93Zcu2KW4NSp3",
    "XC4p4eWfLgff1VuXL7g0VdFm4wUUHqYUqQJAZLmqpjdyBeO3tZIw6vu5meTgMvEE",
    "ygdos+vr0sa3NlUyMKWYNwznqgstQYpkYHf+WkPBS2qIE6iv+qUDLSCCOQJAESSk",
    "CFYxUBJQ7BBs9+Mb/Kppa9Ppuobxf85ZaAq8pYScrLeJKZzYJ8VX2I2aQX/jISLT",
    "YW41qFRd9n9lEkGkWQJAcxPmNI+2r5zJG+K148LLmWCIDTVZ4nxOcxffHka/3tCJ",
    "lDGUw4p2wU6pVRDpNfKrF5Nc9ZKO8NAtC17ZvDyVkQ==",
    "-----END RSA PRIVATE KEY-----",
])

# Private key encrypted with the password 'password'
PEM_ENCRYPTED = u'\n'.join([
    "-----BEGIN RSA PRIVATE KEY-----",
    "Proc-Type: 4,ENCRYPTED",
    "DEK-Info: DES-EDE3-CBC,7CB7069233655F1A",
    "",
    "EpKWFhHefxQLlKS1M6fPXLUVW0gcrHwYNd2q/0J4emhrHmO50KTC6/nVGTvYS1VC",
    "XQwzlla04Ed7kAuP7nkbvT+/6fS72iZmIO/kuhihjaMmRV+peznjEroErndRzWko",
    "LCpe70/yMrHhULGR1lLINe+dZddESfYRoGEM1IYhPEEchXZBdqThvaThgeyVmoAV",
    "A5qhBOP4QFPSV4J0Jd28wTy+uPmGgCjvfvXjx4JZ2LAfPnLXOoKotRqb/cOtMapp",
    "9EmsvjRZH3OLreeQm1BmVzcXGgHLIZWmybGNAW/M0seqeD+NRPXEACOBahXZsSwd",
    "krnWALTkcfLw4NXgaHKdsogDV7gWlwkXr05CrSim0+zvg+hQpVp6Phg9qrT3Jh8g",
    "988v4Fx/rlVdEpfEeXAmLUpXH3jjeyU1ZOyi8c91Vobxe1dJ9G9P8YBBqnZo1xDa",
    "q89FR852v2DKR3xv+GRpzFM43NlWLck9DcNcqIUpbrGd0qRA1k87ZwYSiUPhBvtJ",
    "dix6XfeqbqVMYiH0K4sEyuXxJ98UqFzNY3bBi9oqvoQWpo0qrRYAzHrmDg/hJbO6",
    "aw8yhe922zw8W9+IQIy2j+ZKkaHSMKqjkIwFxmig5EA+mHNDIP4HwlCxA2e2w6HG",
    "ykLE01aHMeS72qRdLVwjib4q2iTEXZVnuyFg/wVprLmLY512iWr03kbj2CVN836b",
    "vEpVIvSj5W6oNXjm+hkKA1AMcHVK96y8Ms3BtarDe4tQDh7GjipkoSXrv+2lIl0o",
    "XjumCv4Gs63Fv3kUr+jo9N3P0SGe1GggX6MOYIcZF0I=",
    "-----END RSA PRIVATE KEY-----",
])

PRIVATE_KEY = Crypto.PublicKey.RSA.importKey(PEM_PRIVATE_KEY)
UNIX_TIMESTAMP = 1435229421


def test_add_pkcs1_padding():
    message = unhexlify(b'f42687f4c3c017ce1e14eceb2ff153ff2d0a9e96')
    padded_message = add_pkcs1_padding(message)

    assert len(padded_message) == 128
    assert (padded_message == unhexlify(
        b'0001ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        b'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        b'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        b'ffffffffffffffffffffff00f42687f4c3c017ce1e14eceb2ff153ff2d0a9e96'
    ))


def test_get_asn1_sequence():
    asn1_sequence = get_asn1_sequence(PRIVATE_KEY)
    assert (asn1_sequence == unhexlify(
        b'30818902818100d7ccfe871ad8cf4b2eee17d3a563b66679f4d529c14bb2ad26'
        b'484cd0ad6e704a236e61cf9da12576396c4f83ed5f55ed7d112e3701492afdb4'
        b'bf82300c2ceba73fabbd15b3c3a23ca1d55b3fe9356a7ed4b7b0f92543422dae'
        b'b67003086d1c2d16684cabc1824d392081ab7c29ba975086947258916a3309bd'
        b'fa20421b541c250203010001'
    ))


def test_calc_key_digest():
    key_digest = calc_key_digest(PRIVATE_KEY)
    assert hexlify(key_digest) == b'4e2a58768ccb6aa06f95e11646e187879d07fb66'


def test_calc_public_key_digest():
    public_key = PRIVATE_KEY.publickey()
    key_digest = calc_key_digest(public_key)
    assert hexlify(key_digest) == b'4e2a58768ccb6aa06f95e11646e187879d07fb66'


def test_calc_permanent_id():
    assert hexlify(calc_permanent_id(PRIVATE_KEY)) == b'4e2a58768ccb6aa06f95'


def test_calc_onion_address():
    assert calc_onion_address(PRIVATE_KEY) == u'jyvfq5umznvka34v'


def test_get_time_period():
    time_period = get_time_period(
        time=UNIX_TIMESTAMP,
        permanent_id=unhexlify(b'4e2a58768ccb6aa06f95'),
    )
    assert time_period == 16611


def test_get_seconds_valid():
    seconds_valid = get_seconds_valid(
        time=UNIX_TIMESTAMP,
        permanent_id=unhexlify(b'4e2a58768ccb6aa06f95'),
    )
    assert seconds_valid == 21054


def test_calc_secret_id_part():
    secret_id_part = calc_secret_id_part(
        time_period=16611,
        descriptor_cookie=None,
        replica=0,
    )
    assert (hexlify(secret_id_part) ==
            b'a0d8e4ec9ac28affed4fa828e8727c7fd4ab4930')


def test_calc_secret_id_part_descriptor_cookie():
    secret_id_part = calc_secret_id_part(
        time_period=16611,
        descriptor_cookie=base64.b64decode('dCmx3qIvArbil8A0KM4KgQ=='),
        replica=0,
    )
    assert (hexlify(secret_id_part) ==
            b'ea4e24b1a832f1da687f874b40fa9ecfe5221dd9')


def test_calc_descriptor_id():
    descriptor_id = calc_descriptor_id(
        permanent_id=b'N*Xv\x8c\xcbj\xa0o\x95',
        secret_id_part=unhexlify(b'a0d8e4ec9ac28affed4fa828e8727c7fd4ab4930'),
    )
    assert (hexlify(descriptor_id) ==
            b'f58ce3c63ee634e1ffaf936251a822ff06385f55')


def test_rounded_timestamp():
    timestamp = datetime.datetime(2015, 6, 25, 13, 13, 25)
    assert rounded_timestamp(timestamp) == u'2015-06-25 13:00:00'


def test_rounded_timestamp_none_specified(monkeypatch):
    # Freeze datetime returned from datetime.datetime.utcnow()
    class frozen_datetime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return datetime.datetime(2015, 6, 25, 13, 13, 25)
    monkeypatch.setattr(datetime, 'datetime', frozen_datetime)
    assert rounded_timestamp(timestamp=None) == u'2015-06-25 13:00:00'


def test_base32_encode_str():
    assert base32_encode_str(byte_str=b'byte input') == u'mj4xizjanfxha5lu'


@pytest.mark.skipif(sys.version_info < (3, 0), reason="python3 only")
def test_base32_encode_str_not_byte_string():
    with pytest.raises(TypeError):
        base32_encode_str(byte_str=u'not a byte string')


def test_key_decrypt_prompt(mocker):
    # Valid private PEM key
    mocker.patch(builtin('open'), lambda *_: io.StringIO(PEM_PRIVATE_KEY))
    key = key_decrypt_prompt('private.key')
    assert isinstance(key, Crypto.PublicKey.RSA._RSAobj)
    assert key.has_private()


def test_key_decrypt_prompt_public_key(mocker):
    # Valid public PEM key
    private_key = Crypto.PublicKey.RSA.importKey(PEM_PRIVATE_KEY)
    pem_public_key = private_key.publickey().exportKey().decode('utf-8')
    mocker.patch(builtin('open'), lambda *_: io.StringIO(pem_public_key))

    with pytest.raises(ValueError):
        key_decrypt_prompt('public.key')


def test_key_decrypt_prompt_malformed_key(mocker):
    mocker.patch(builtin('open'), lambda *_: io.StringIO(PEM_INVALID_KEY))
    with pytest.raises(ValueError):
        key_decrypt_prompt('private.key')


def test_key_decrypt_prompt_incorrect_size(mocker):
    # Key which is not 1024 bits
    private_key_1280 = Crypto.PublicKey.RSA.generate(1280)
    pem_key_1280 = private_key_1280.exportKey().decode('utf-8')
    mocker.patch(builtin('open'), lambda *_: io.StringIO(pem_key_1280))
    with pytest.raises(ValueError):
        key_decrypt_prompt('512-bit-private.key')


def test_key_decrypt_prompt_encrypted(mocker):
    mocker.patch(builtin('open'), lambda *_: io.StringIO(PEM_ENCRYPTED))

    # Load with correct password
    mocker.patch('getpass.getpass', lambda *_: u'password')
    key = key_decrypt_prompt('encrypted_private.key')
    assert isinstance(key, Crypto.PublicKey.RSA._RSAobj)

    # Load with incorrect password
    mocker.patch('getpass.getpass', lambda *_: u'incorrect password')
    with pytest.raises(ValueError):
        key_decrypt_prompt('encrypted_private.key')


def test_try_make_dir_makedirs(mocker):
    mocker.patch('os.makedirs')
    try_make_dir('dir')
    os.makedirs.assert_called_once_with('dir')


def test_try_make_dir_makedirs_dir_already_exists(mocker):
    mocker.patch('os.makedirs', side_effect=OSError)
    mocker.patch('os.path.isdir', return_value=True)
    try_make_dir('dir')
    os.path.isdir.assert_called_once_with('dir')


def test_try_make_dir_makedirs_dir_other_error(mocker):
    mocker.patch('os.makedirs', side_effect=OSError)
    mocker.patch('os.path.isdir', return_value=False)
    with pytest.raises(OSError):
        try_make_dir('dir')


def test_is_directory_empty_empty(mocker):
    # Directory is empty
    mocker.patch('os.listdir', return_value=[])
    assert is_directory_empty('dir_empty/')


def test_is_directory_empty_not_empty(mocker):
    # Directory is empty
    mocker.patch('os.listdir', return_value=['filename'])
    assert not is_directory_empty('dir_not_empty/')
