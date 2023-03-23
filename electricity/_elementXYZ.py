# 元件坐标系
# 一个非门的长为0.15，宽为0.075
# 一个非门的长宽会成为元件坐标系的x, y的单位长度
# z轴的单位长度是原坐标系的0.1
#
# 像二位乘法器这种元件的位置必须经过修正才能使元件整齐排列
# x, z轴不用修正
# y轴的修正为 +0.045

# _elementClassHead里的element_Init_HEAD有部分处理元件坐标系的代码
# crt_Experiment也有部分代码

from typing import Union

### define ###
elementXYZ = False
# 物实坐标系x, y, z单位1
_xUnit = 0.16
_yUnit = 0.08
_zUnit = 0.1
# big_element坐标修正
_xAmend = 0.04
### end define ###

# 将元件坐标系转换为物实支持的坐标系
def xyzTranslate(x: Union[int, float], y: Union[int, float], z: Union[int, float], isBigElement = False):
    x *= _xUnit
    y *= _yUnit
    z *= _zUnit
    if isBigElement:
        y += _xAmend
    return x, y, z

# 将物实支持的坐标系转换为元件坐标系
def translateXYZ(x: Union[int, float], y: Union[int, float], z: Union[int, float], isBigElement = False):
    x /= _xUnit
    y /= _yUnit
    z /= _zUnit
    if isBigElement:
        y -= _xAmend
    return x, y, z

def set_elementXYZ(boolen: bool):
    global elementXYZ
    elementXYZ = bool(boolen)