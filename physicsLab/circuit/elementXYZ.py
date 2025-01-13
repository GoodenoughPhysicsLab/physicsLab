# -*- coding: utf-8 -*-
# 元件坐标系
# 元件坐标系的单位x为一个是门的长
# 单位y是一个是门的宽
# 单位z为物实默认坐标系的0.1

from physicsLab import errors
from physicsLab._tools import position
from physicsLab.typehint import num_type
from physicsLab._core import get_current_experiment
from physicsLab.enums import ExperimentType

# 是否将全局设置为元件坐标系
def set_elementXYZ(boolen: bool) -> None:
    # 这玩意是否也有必要塞进构造函数里?
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

def xyzTranslate(x: num_type, y: num_type, z: num_type, is_bigElement: bool = False):
    ''' 将元件坐标系转换为物实的坐标系 '''
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    x *= _X_UNIT
    y *= _Y_UNIT
    z *= _Z_UNIT
    if is_bigElement:
        x, y, z = amend_big_Element(x, y, z)
    return x, y, z

def translateXYZ(x: num_type, y: num_type, z: num_type, is_bigElement: bool = False):
    ''' 将物实的坐标系转换为元件坐标系 '''
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    x /= _X_UNIT
    y /= _Y_UNIT
    z /= _Z_UNIT
    # 修改大体积逻辑电路元件的坐标
    if is_bigElement:
        y -= _Y_AMEND
    return x, y, z

# 修正bigElement的坐标
def amend_big_Element(x: num_type, y: num_type, z: num_type):
    return x, y + _Y_AMEND, z

def get_xyzUnit() -> tuple:
    ''' 获取元件坐标系下的单位长度对应着物实坐标系下的值
    '''
    return _X_UNIT, _Y_UNIT, _Z_UNIT
