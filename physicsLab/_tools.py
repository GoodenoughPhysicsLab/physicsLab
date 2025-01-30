# -*- coding: utf-8 -*-
from random import choice
from string import ascii_lowercase, ascii_letters, digits

from collections import namedtuple
from ._typing import num_type

# TODO 元件坐标系也应该由这玩意负责
position = namedtuple("position", ["x", "y", "z"])

def round_data(num: num_type) -> num_type:
    if not isinstance(num, (int, float)):
        raise TypeError
    return round(num, 6)

def randString(length: int, is_lower: bool = False) -> str:
    if not isinstance(length, int) \
            or not isinstance(is_lower, bool):
        raise TypeError

    if is_lower:
        letters = ascii_lowercase
    else:
        letters = ascii_letters
    return ''.join(choice(letters + digits) for _ in range(length))
