#coding=utf-8
import typing as _typing

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