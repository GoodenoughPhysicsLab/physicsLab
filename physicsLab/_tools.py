#coding=utf-8
import typing as _typing
import unittest as _unittest

# type hint
numType = _typing.Union[int, float]

# 四舍五入physicsLab中的数据
# 支持传入多个数据
def roundData(*num):
    if not any(
        isinstance(i, (int, float)) for i in num
     ):
        raise TypeError
    
    if len(num) == 1:
        return round(num[0], 4)
    return (round(i, 4) for i in num)

# 生成随机字符串
def randString(strLength: int) -> str:
    if not isinstance(strLength, int):
        raise TypeError

    from string import ascii_letters as _ascii_letters, digits as _digits
    from random import choice as _choice
    return ''.join(_choice(_ascii_letters + _digits) for _ in range(strLength))

# 设置只读属性，未测试，开发中
class const:
    def __init__(self, val: _typing.Any) -> None:
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