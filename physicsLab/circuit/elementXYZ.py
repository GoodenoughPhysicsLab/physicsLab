# -*- coding: utf-8 -*-
# 元件坐标系
# 元件坐标系的单位x为一个是门的长
# 单位y是一个是门的宽
# 单位z为物实默认坐标系的0.1

import physicsLab._tools as _tools
import physicsLab.phy_errors as phy_errors

from physicsLab.experiment import stack_Experiment
from physicsLab.experimentType import experimentType

# 全局是否为elementXYZ
_elementXYZ: bool = False

# 是否将全局设置为元件坐标系
def set_elementXYZ(boolen: bool) -> None:
    if stack_Experiment.top().ExperimentType != experimentType.Circuit:
        raise phy_errors.ExperimentTypeError
    if not isinstance(boolen, bool):
        raise TypeError
    global _elementXYZ
    _elementXYZ = boolen

# 获取是否为元件坐标系
def is_elementXYZ() -> bool:
    return _elementXYZ

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
    if stack_Experiment.top().ExperimentType != experimentType.Circuit:
        raise phy_errors.ExperimentTypeError

    x *= _xUnit
    y *= _yUnit
    z *= _zUnit
    # 修改元件坐标系原点
    x += _xOrigin
    y += _yOrigin
    z += _zOrigin
    return x, y, z

# 将物实支持的坐标系转换为元件坐标系
def translateXYZ(x: _tools.numType, y: _tools.numType, z: _tools.numType, bigElement: bool = False):
    if stack_Experiment.top().ExperimentType != experimentType.Circuit:
        raise phy_errors.ExperimentTypeError

    x /= _xUnit
    y /= _yUnit
    z /= _zUnit
    # 修改元件坐标系原点
    x -= _xOrigin
    y -= _yOrigin
    z -= _zOrigin
    # 修改大体积逻辑电路原件的坐标
    if bigElement:
        # 暂不支持相关功能
        pass
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

# 输入"x" 返回_xUnit
# 输入"y", "z" 返回_yUnit, _zUnit
def get_xyzUnit(*args):
    if any(i not in ("x", "y", "z") for i in args):
        raise TypeError
    index = {
        "x": _xUnit,
        "y": _yUnit,
        "z": _zUnit
    }
    if len(args) == 1:
        return index[args[0]]
    return (index[string] for string in args)