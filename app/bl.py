import math

from string import digits, ascii_lowercase, ascii_uppercase


DIGITS = digits + ascii_lowercase + ascii_uppercase
BASE = len(DIGITS)

DIGITS_OFFSET = 48
LOWERCASE_OFFSET = 87
UPPERCASE_OFFSET = 29


def to_base(num):
    """
    Converts integer number to base 62.

    :param num: integer > 0 
    :return: string that represent `num' in base 62

    >>> to_base(1)
    '4GFfc4'
    >>> to_base(42)
    '3aTWiaI'
    >>> to_base(150)
    'bldMLbG'
    >>> to_base(1984)
    '2q1hQe40'
    """

    # NOTE: here we suppose that num always > 0.
    num = perfect_hash(num)
    chars = []
    while num > 0:
        chars.append(DIGITS[num % BASE])
        num //= BASE
    return ''.join(reversed(chars))


def from_base(num_str):
    """
    Converts string that represent a number in base 62 to integer in base 10.

    :param num_str: string that represent a number in base 62 
    :return: integer in base 10

    >>> from_base('4GFfc4')
    1
    >>> from_base('3aTWiaI')
    42
    >>> from_base('bldMLbG')
    150
    >>> from_base('2q1hQe40')
    1984
    """
    res = 0
    for idx, char in enumerate(reversed(num_str)):
        if char.isdigit():
            num = ord(char) - DIGITS_OFFSET
        elif 'a' <= char <= 'z':
            num = ord(char) - LOWERCASE_OFFSET
        elif 'A' <= char <= 'Z':
            num = ord(char) - UPPERCASE_OFFSET
        else:
            return -1
        res += num * int(math.pow(BASE, idx))
    return perfect_hash(res)


def perfect_hash(n):
    # perfect_hash(perfect_hash(n)) == n
    return (
        ((0x00000000FFFFFFFF & n) << 32) +
        ((0xFFFFFFFF00000000 & n) >> 32)
    )
