# -*- coding: utf-8 -*-
''' 元件坐标系
    元件坐标系的单位x为一个是门的长
    单位y是一个是门的宽
    单位z为物实默认坐标系的0.1
'''
from physicsLab import errors
from physicsLab.typehint import num_type
from physicsLab._core import get_current_experiment
from physicsLab.enums import ExperimentType

# 是否将全局设置为元件坐标系
def set_elementXYZ(status: bool) -> None:
    # 这玩意是否也有必要塞进构造函数里?
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError
    if not isinstance(status, bool):
        raise TypeError

    get_current_experiment().is_elementXYZ = status

# 物实坐标系x, y, z单位1
_X_UNIT: float = 0.16
_Y_UNIT: float = 0.08
_Z_UNIT: float = 0.1
# big_element坐标修正
_Y_AMEND: float = 0.045

def xyzTranslate(x: num_type, y: num_type, z: num_type, is_bigElement: bool = False):
    ''' 将元件坐标系转换为物实的坐标系 '''
    if get_current_experiment().experiment_type != ExperimentType.Circuit:
        raise errors.ExperimentTypeError

    x *= _X_UNIT
    y *= _Y_UNIT
    z *= _Z_UNIT
    if is_bigElement:
        y += _Y_AMEND
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

def get_xyzUnit() -> tuple:
    ''' 获取元件坐标系下的单位长度对应着物实坐标系下的值
    '''
    return _X_UNIT, _Y_UNIT, _Z_UNIT
