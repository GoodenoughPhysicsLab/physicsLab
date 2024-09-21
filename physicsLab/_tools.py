# -*- coding: utf-8 -*-
from random import choice
from string import ascii_lowercase, ascii_letters, digits

from collections import namedtuple
from .typehint import Tuple, Union, numType

position = namedtuple("position", ["x", "y", "z"])

# 四舍五入physicsLab中的数据
# 支持传入多个数据
def roundData(*num) -> Union[numType, Tuple[numType]]:
    if not all(isinstance(val, (int, float)) for val in num):
        raise TypeError

    if len(num) == 1:
        return round(num[0], 4)
    return tuple(round(i, 4) for i in num)

# 生成随机字符串
def randString(strLength: int, lower: bool = False) -> str:
    if not isinstance(strLength, int):
        raise TypeError

    if lower:
        letters = ascii_lowercase
    else:
        letters = ascii_letters
    return ''.join(choice(letters + digits) for _ in range(strLength))
