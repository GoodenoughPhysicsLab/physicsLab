#coding=utf-8
import typing

# type hint
number = typing.Union

# 四舍五入physicsLab中的数据
def roundData(num: number):
    # if isinstance(num, int):
    #     return float(num)
    return round(num, 4)

# 生成随机字符串
def randString(strLength: int) -> str:
    if not isinstance(strLength, int):
        raise TypeError

    from string import ascii_letters as _ascii_letters, digits as _digits
    from random import choice as _choice
    return ''.join(_choice(_ascii_letters + _digits) for _ in range(strLength))