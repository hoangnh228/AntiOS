import os
import logging
import string
import log_helper
import identity_data
import random
import time
import datetime
import itertools
import platform
import binascii

logger = log_helper.setup_logger(name="random_utils", level=logging.DEBUG, log_to_file=False)


__doc__ = """Service functions for generation random values and sequences with given format.
Hostname, user name and MAC address, randomly selected from lists imported from identity_data module,
random unix time, random string sequences. Helper functions for writing special values to Windows registry
Also is_x64os() helper function provided
"""


def is_x64os():
    """
    :return: True if system is 64-bit, False otherwise
    """
    return platform.machine().endswith('64')


def random_hostname():
    """
    :return: random host name from the list
    """
    logger.info("Length of hostname list is {0}".format(len(identity_data.HOSTNAMES)))
    return random.choice(identity_data.HOSTNAMES)


def random_username():
    """
    :return: random user name from the list
    """
    logger.info("Length of username list is {0}".format(len(identity_data.USERNAMES)))
    return random.choice(identity_data.USERNAMES)


def random_mac_address():
    """
    :return: random user name from the list
    """
    logger.info("Length of MAC addresses list is {0}".format(len(identity_data.MAC_ADDRESSES)))
    return random.choice(identity_data.MAC_ADDRESSES)


def random_unix_time(from_date, to_date):
    """
    :return: Random Unix Time from the assigned dates interval
    Dates should be in DD.MM.YYYY string format, e.g. ("01.01.2005", "01.01.2018")
    """
    from_unix = int(time.mktime(datetime.datetime.strptime(from_date, "%d.%m.%Y").timetuple()))
    to_unix = int(time.mktime(datetime.datetime.strptime(to_date, "%d.%m.%Y").timetuple()))
    return random.randint(from_unix, to_unix)


def random_digit_string(length):
    """
    :param length: size of generated string
    :return: random string of digits
    """
    return ''.join(random.choices(string.digits, k=length))


def disperse_string(solid_string):
    """
    Function converts string to list "dispersed" with zeroes.
    Function is necessary for writing special values to Windows registry
    :param solid_string: normal 0-ended string, like "123"
    :return: list dispersed with zeroes, like ['1', 0, '2', 0, '3', 0]
    """
    normal_list = list(solid_string)
    return list(itertools.chain.from_iterable(zip(normal_list, [0] * len(normal_list))))


def bytes_list_to_array(bytes_list):
    """
    Convert bytes list, which is Python list with values in range [0, 255], to binary array.
    Function is necessary for writing special values to Windows registry
    :param bytes_list: Python list with values in range [0, 255], like [0, 1, 255, 'A', ...]
    :return: binary array b'0x000x01...'
    """
    digital_bytes = []
    for elem in bytes_list:
        if isinstance(elem, int):
            digital_bytes.append(elem.to_bytes(1, 'little'))
        elif isinstance(elem, str):
            digital_bytes.append(ord(elem).to_bytes(1, 'little'))
    digital_bytes_array = b''.join(digital_bytes)
    return digital_bytes_array


def random_volume_id():
    """
    :return: Random Volume ID, XXXX-XXXX, where X is a series of numbers and letters
    """
    x1 = str(binascii.b2a_hex(os.urandom(2)))
    x2 = str(binascii.b2a_hex(os.urandom(2)))
    return "{0}-{1}".format(x1, x2)
