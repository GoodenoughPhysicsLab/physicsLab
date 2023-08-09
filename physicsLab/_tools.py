#coding=utf-8
from os import walk
from typing import *
from collections import namedtuple
from physicsLab._fileGlobals import FILE_HEAD

# type hint
numType = Union[int, float]

# class position
position = namedtuple("position", ["x", "y", "z"])

# 四舍五入physicsLab中的数据
# 支持传入多个数据
def roundData(*num) -> Union[float, Tuple[float]]:
    if not all(isinstance(val, (int, float)) for val in num):
        raise TypeError
    
    if len(num) == 1:
        return float(round(num[0], 4))
    return tuple(float(round(i, 4)) for i in num)

# 生成随机字符串
def randString(strLength: int) -> str:
    if not isinstance(strLength, int):
        raise TypeError

    from string import ascii_letters as _ascii_letters, digits as _digits
    from random import choice as _choice
    return ''.join(_choice(_ascii_letters + _digits) for _ in range(strLength))

# 索取所有物实存档
def getAllSav() -> List:
    savs = [i for i in walk(FILE_HEAD)][0]
    savs = savs[savs.__len__() - 1]
    return [aSav for aSav in savs if aSav.endswith('sav')]