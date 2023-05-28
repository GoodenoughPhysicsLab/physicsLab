#coding=utf-8
from typing import *
import unittest as _unittest
from os import walk
from physicsLab._fileGlobals import FILE_HEAD

# type hint
numType = Union[int, float]

# 四舍五入physicsLab中的数据
# 支持传入多个数据
def roundData(*num) -> Union[int, float, tuple]:
    if not any(
        isinstance(i, (int, float)) for i in num
     ):
        raise TypeError
    
    if len(num) == 1:
        return round(num[0], 4)
    return tuple(round(i, 4) for i in num)

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

# 设置只读属性，未测试，开发中
class const:
    def __init__(self, val: Any) -> None:
        self.val = val

    def __get__(self, instance, owner):
        return self.val

# 仅供测试。因为_tools是package私有的，因此无法在包外测试
if __name__ == "__main__":
    # run test
    _unittest.main()

class myTestCase(_unittest.TestCase):
    def test_const(self):
        a = const(5)
        print(a)