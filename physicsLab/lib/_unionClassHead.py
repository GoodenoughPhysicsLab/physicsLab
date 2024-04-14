# -*- coding: utf-8 -*-
from physicsLab import errors
from physicsLab.circuit import elements
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab._tools import roundData
from physicsLab.typehint import numType, Optional
from physicsLab.experiment import stack_Experiment
from physicsLab.experimentType import experimentType

class UnionMeta(type):
    def __call__(cls,
                 x: numType = 0,
                 y: numType = 0,
                 z: numType = 0,
                 bitLength: int = 4,
                 elementXYZ: Optional[bool] = None,  # x, y, z是否为元件坐标系
                 unionHeading: bool = False,  # False: 生成的元件为竖直方向，否则为横方向
                 fold: bool = False,  # False: 生成元件时不会在同一水平面的元件超过一定数量后z + 1继续生成元件
                 foldMaxNum: int = 4,  # 达到foldMaxNum个元件数时即在z轴自动折叠
                 *args, **kwags
    ):
        self = cls.__new__(cls)
        if stack_Experiment.top().ExperimentType != experimentType.Circuit:
            raise errors.ExperimentTypeError

        if foldMaxNum <= 0 or not(
            isinstance(x, (int, float)) or
            isinstance(y, (int, float)) or
            isinstance(z, (int, float)) or
            isinstance(elementXYZ, bool) or
            isinstance(unionHeading, bool) or
            isinstance(fold, bool) or
            isinstance(foldMaxNum, int)
        ):
            raise TypeError
        if not isinstance(bitLength, int) or bitLength < 1:
            raise errors.bitLengthError("bitLength must get a integer")

        # 元件坐标系，如果输入坐标不是元件坐标系就强转为元件坐标系
        if not (elementXYZ is True or (_elementXYZ.is_elementXYZ() is True and elementXYZ is None)):
            x, y, z = _elementXYZ.translateXYZ(x, y, z)
        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple

        self.__init__(x, y, z, bitLength, elementXYZ, unionHeading, fold, foldMaxNum, *args, **kwags)
        if not hasattr(self, "_elements"):
            raise AttributeError

        return self

# Union class的基类 MixIn Class
class UnionBase(metaclass=UnionMeta):
    # 此类无法被实例化
    def __init__(self, *args, **kwargs):
        raise errors.instantiateError

    # 获取以模块化电路生成顺序为item的原件的self
    # 一定有self._elements
    def __getitem__(self, item: int) -> "elements.CircuitBase":
        if not isinstance(item, int):
            raise TypeError
        return self._elements[item] # type: ignore -> 子类含有._elements

    # 设置坐标
    def set_Position(self, x, y, z):
        pass