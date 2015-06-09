# -*- coding: utf-8 -*-
import hashlib
import struct
import datetime
import getpass
import base64
import binascii

# import Crypto.Util
import Crypto.PublicKey


def add_pkcs1_padding(message):
    """Add PKCS#1 padding to **message**."""
    padding = b''
    typeinfo = b'\x00\x01'
    separator = b'\x00'
    for x in range(125 - len(message)):
        padding += b'\xFF'
    PKCS1paddedMessage = typeinfo + padding + separator + message
    assert len(PKCS1paddedMessage) == 128
    return PKCS1paddedMessage


def get_asn1_sequence(rsa_key):
    seq = Crypto.Util.asn1.DerSequence()
    seq.append(rsa_key.n)
    seq.append(rsa_key.e)
    asn1_seq = seq.encode()
    return asn1_seq


def calc_key_digest(rsa_key):
    """Calculate the SHA1 digest of an RSA key"""
    return hashlib.sha1(get_asn1_sequence(rsa_key)).digest()


def calc_permanent_id(rsa_key):
    return calc_key_digest(rsa_key)[:10]


def calc_onion_address(rsa_key):
    return base64.b32encode(calc_permanent_id(rsa_key)).decode().lower()


def calc_descriptor_id(permanent_id, secret_id_part):
    return hashlib.sha1(permanent_id + secret_id_part).digest()


def get_time_period(time, permanent_id):
    """
    time-period = (current-time + permanent-id-byte * 86400 / 256) / 86400
    """
    permanent_id_byte = int(struct.unpack('B', permanent_id[0:1])[0])
    return int((int(time) + permanent_id_byte * 86400 / 256) / 86400)


def get_seconds_valid(time, permanent_id):
    """
    Calculate seconds until the descriptor ID changes
    """
    permanent_id_byte = int(struct.unpack('B', permanent_id[0:1])[0])
    return 86400 - int((int(time) + permanent_id_byte * 86400 / 256) % 86400)


def calc_secret_id_part(time_period, descriptor_cookie, replica):
    """
    secret-id-part = H(time-period | descriptor-cookie | replica)
    """
    secret_id_part = hashlib.sha1()
    secret_id_part.update(struct.pack('>I', time_period)[:4])
    if descriptor_cookie:
        secret_id_part.update(descriptor_cookie)
    secret_id_part.update(binascii.unhexlify('{0:02X}'.format(replica)))
    return secret_id_part.digest()


def rounded_timestamp(timestamp=None):
    """
    Create timestamp rounded down to the nearest hour
    """
    if not timestamp:
        timestamp = datetime.datetime.utcnow()
    timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def base32_encode_str(bytes):
    """
    Encode bytes as lowercase base32 string
    """
    return base64.b32encode(bytes).lower().decode('utf-8')


def key_decrypt_prompt(key_file, retries=3):
    """
    Try open an PEM encrypted private key, propmpting the user for a
    passphrase if required.
    """

    for retries in range(0, retries):
        key_passphrase = None
        with open(key_file, 'r') as handle:
            pem_key = handle.read()

            if "Proc-Type: 4,ENCRYPTED" in pem_key:  # Key looks encrypted
                key_passphrase = getpass.getpass(
                    "Enter the password for the private key (%s): " % key_file)
            try:
                permanent_key = Crypto.PublicKey.RSA.importKey(
                    pem_key, passphrase=key_passphrase)
            except ValueError:
                # Key not decrypted correctly, prompt for passphrase again
                continue
            else:
                return permanent_key

    # No private key was imported
    raise ValueError("Could not import RSA key")
