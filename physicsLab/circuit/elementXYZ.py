# -*- coding: utf-8 -*-
# 元件坐标系
# 元件坐标系的单位x为一个是门的长
# 单位y是一个是门的宽
# 单位z为物实默认坐标系的0.1

from physicsLab import errors
from physicsLab._tools import position
from physicsLab.typehint import numType
from physicsLab.Experiment import get_current_experiment
from physicsLab.enums import ExperimentType

# 是否将全局设置为元件坐标系
def set_elementXYZ(boolen: bool) -> None:
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError
    if not isinstance(boolen, bool):
        raise TypeError

    get_current_experiment().is_elementXYZ = boolen

# 获取是否为元件坐标系
def is_elementXYZ() -> bool:
    return get_current_experiment().is_elementXYZ # TODO: 将电学专有的attr放在支持3大实验的Experiment中是否合适?

# 物实坐标系x, y, z单位1
_X_UNIT: float = 0.16
_Y_UNIT: float = 0.08
_Z_UNIT: float = 0.1
# big_element坐标修正
_Y_AMEND = 0.045

def xyzTranslate(x: numType, y: numType, z: numType, is_bigElement: bool = False):
    ''' 将元件坐标系转换为物实的坐标系 '''
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    _xOrigin, _yOrigin, _zOrigin = get_OriginPosition()

    x *= _X_UNIT
    y *= _Y_UNIT
    z *= _Z_UNIT
    # 修改元件坐标系原点
    x += _xOrigin
    y += _yOrigin
    z += _zOrigin
    if is_bigElement:
        x, y, z = amend_big_Element(x, y, z)
    return x, y, z

def translateXYZ(x: numType, y: numType, z: numType, is_bigElement: bool = False):
    ''' 将物实的坐标系转换为元件坐标系 '''
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    _xOrigin, _yOrigin, _zOrigin = get_OriginPosition()

    x /= _X_UNIT
    y /= _Y_UNIT
    z /= _Z_UNIT
    # 修改元件坐标系原点
    x -= _xOrigin
    y -= _yOrigin
    z -= _zOrigin
    # 修改大体积逻辑电路原件的坐标
    if is_bigElement:
        y -= _Y_AMEND
    return x, y, z

# 设置元件坐标系原点O，输入值为物实坐标系
def set_O(x: numType, y: numType, z: numType) -> None:
    if (isinstance(x, (int, float)) and
        isinstance(y, (int, float)) and
        isinstance(z, (int, float))
    ):
        get_current_experiment().elementXYZ_origin_position = position(x, y, z)
    else:
        raise TypeError

# 修正bigElement的坐标
def amend_big_Element(x: numType, y: numType, z: numType):
    return x, y + _Y_AMEND, z

# 获取坐标原点
def get_OriginPosition() -> position:
    return get_current_experiment().elementXYZ_origin_position

def get_xyzUnit() -> tuple:
    ''' 获取元件坐标系下的单位长度对应着物实坐标系下的值
    '''
    return _X_UNIT, _Y_UNIT, _Z_UNIT
