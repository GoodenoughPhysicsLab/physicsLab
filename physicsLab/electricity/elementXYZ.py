#coding=utf-8
# 元件坐标系
# 一个非门的长为0.16，宽为0.08
# 一个非门的长宽会成为元件坐标系的x, y的单位长度
# z轴的单位长度是原坐标系的0.1
#
# 像二位乘法器这种元件的位置必须经过修正才能使元件整齐排列
# x, z轴不用修正
# y轴的修正为 +0.04
# 坐标修正部分的代码在对应的类的文件中
# 如big_Elements的坐标修正在logicCircuit.py

# _elementClassHead里的element_Init_HEAD有部分处理元件坐标系的代码，并调用了该文件

import physicsLab._tools as _tools

### define ###

# 是否将全局设置为元件坐标系
elementXYZ: bool = False

def set_elementXYZ(boolen: bool) -> None:
    if not isinstance(boolen, bool):
        raise TypeError
    global elementXYZ
    elementXYZ = boolen

# 物实坐标系x, y, z单位1
_xUnit: _tools.numType = 0.16
_yUnit: _tools.numType = 0.08
_zUnit: _tools.numType = 0.1
# big_element坐标修正
_yAmend = 0.045

# 元件坐标系原点
_xOrigin, _yOrigin, _zOrigin = 0, 0, 0

### end define ###

# 将元件坐标系转换为物实支持的坐标系
def xyzTranslate(x: _tools.numType, y: _tools.numType, z: _tools.numType):
    x *= _xUnit
    y *= _yUnit
    z *= _zUnit
    # 修改元件坐标系原点
    x += _xOrigin
    y += _yOrigin
    z += _zOrigin
    return x, y, z

# 将物实支持的坐标系转换为元件坐标系
def translateXYZ(x: _tools.numType, y: _tools.numType, z: _tools.numType):
    x /= _xUnit
    y /= _yUnit
    z /= _zUnit
    # 修改元件坐标系原点
    x -= _xOrigin
    y -= _yOrigin
    z -= _zOrigin
    # 修改大体积逻辑电路原件的坐标
        # 暂不支持相关功能
    return x, y, z

# 设置元件坐标系原点O，输入值为物实坐标系
def set_O(x: _tools.numType, y: _tools.numType, z: _tools.numType) -> None:
    if (isinstance(x, (int, float)) and
        isinstance(y, (int, float)) and
        isinstance(z, (int, float))
    ):
        global _xOrigin, _yOrigin, _zOrigin
        _xOrigin, _yOrigin, _zOrigin = x, y, z
    else:
        raise TypeError

# 修正bigElement的坐标
def amend_big_Element(
        x: _tools.numType,
        y: _tools.numType, 
        z: _tools.numType
    ):
    return x, y + _yAmend, z

# 获取坐标原点
def get_OriginPosition():
    return _xOrigin, _yOrigin, _zOrigin