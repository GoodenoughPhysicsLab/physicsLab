# -*- coding: utf-8 -*-
import inspect

from physicsLab import errors
from physicsLab import _tools
from physicsLab.circuit import wire
from physicsLab.elementBase import ElementBase
import physicsLab.circuit.elementXYZ as _elementXYZ

from physicsLab.enums import ExperimentType
from physicsLab.typehint import Optional, Self, numType, CircuitElementData, Generate
from physicsLab._tools import roundData, randString
from physicsLab.experiment import Experiment, get_Experiment

# electricity class's metaClass
class CircuitMeta(type):
    def __call__(cls,
                 x: numType,
                 y: numType,
                 z: numType,
                 elementXYZ: Optional[bool] = None,
                 *args, **kwargs
                ):
        self = cls.__new__(cls) # type: ignore -> create subclass of electricityBase
        if not (
                isinstance(x, (float, int)) and
                isinstance(y, (float, int)) and
                isinstance(z, (float, int)) and
                (elementXYZ is None or isinstance(elementXYZ, bool))
        ):
            raise TypeError

        _Expe: Experiment = get_Experiment()
        self.experiment = _Expe

        if _Expe.experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError

        self.is_elementXYZ = False # 元件坐标系

        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple
        self._position = _tools.position(x, y, z) # type: ignore
        # 元件坐标系
        if elementXYZ is True or _elementXYZ.is_elementXYZ() is True and elementXYZ is None:
            x, y, z = _elementXYZ.xyzTranslate(x, y, z)
            self.is_elementXYZ = True

        self.__init__(x, y, z, elementXYZ, *args, **kwargs)
        assert hasattr(self, "data")

        # 若是big_Element，则修正坐标
        if self.is_elementXYZ and self.is_bigElement:
            x, y, z = _elementXYZ.amend_big_Element(x, y, z)

        self.data["Identifier"] = randString(32)
        # x, z, y 物实采用欧拉坐标系
        self.data["Position"] = f"{x},{z},{y}"

        # 该坐标是否已存在，则存入列表
        if self._position in _Expe.elements_Position.keys():
            _Expe.elements_Position[self._position].append(self)
        else:
            _Expe.elements_Position[self._position] = [self]
        self.set_Rotation()

        _Expe.Elements.append(self)

        return self

# 所有电学元件的父类
class CircuitBase(ElementBase, metaclass=CircuitMeta):
    is_bigElement = False # 该元件是否是逻辑电路的两体积元件

    def __init__(self) -> None:
        raise RuntimeError("can not init virtual class")

    def __define_virtual_var_to_let_ide_show(self,
                                             data: CircuitElementData,
                                             exp: Experiment):
        ''' useless
            这些变量的定义在CircuitMeta中
        '''
        self.data: CircuitElementData = data
        self.experiment: Experiment = exp

    def __repr__(self) -> str:
        return  f"{self.__class__.__name__}" \
                f"({self._position.x}, {self._position.y}, {self._position.z}, " \
                f"elementXYZ={self.is_elementXYZ})"

    def set_Rotation(self, xRotation: numType = 0, yRotation: numType = 0, zRotation: numType = 180) -> Self:
        ''' 设置原件的角度 '''
        if not (
                isinstance(xRotation, (int, float)) and
                isinstance(yRotation, (int, float)) and
                isinstance(zRotation, (int, float))
        ):
            raise TypeError

        self.data["Rotation"] = f"{roundData(xRotation)},{roundData(zRotation)},{roundData(yRotation)}"
        return self

    # 重新设置元件的坐标
    def set_Position(self, x: numType, y: numType, z: numType, elementXYZ: Optional[bool] = None) -> Self:
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise TypeError
        x, y, z = roundData(x, y, z) # type: ignore -> result type: tuple

        self._position = _tools.position(x, y, z)

        #元件坐标系
        if elementXYZ is True or _elementXYZ.is_elementXYZ() is True and elementXYZ is None:
            x, y, z = _elementXYZ.xyzTranslate(x, y, z, self.is_bigElement)
            self.is_elementXYZ = True

        for _, self_list in get_Experiment().elements_Position.items():
            if self in self_list:
                self_list.remove(self)

        self.data['Position'] = f"{x},{z},{y}" # type: ignore

        _Expe = get_Experiment()
        if self._position in _Expe.elements_Position.keys():
            _Expe.elements_Position[self._position].append(self)
        else:
            _Expe.elements_Position[self._position] = [self]

        return self

    # 获取原件的坐标
    def get_Position(self) -> tuple:
        return self._position

    # 获取元件的index（每创建一个元件，index就加1）
    def get_Index(self) -> int:
        return self.experiment.Elements.index(self) + 1

    # 获取子类的类型
    @property
    def modelID(self) -> str:
        assert not isinstance(self.data['ModelID'], type(Generate))
        return self.data['ModelID']

    @classmethod
    def _get_property(cls) -> list:
        res: list = []
        for name, _ in inspect.getmembers(cls, lambda i: isinstance(i, property)):
            res.append(name)

        return res

# 双引脚模拟电路原件的基类
class TwoPinMixIn(CircuitBase):
    @property
    def red(self) -> wire.Pin:
        return wire.Pin(self, 0)

    @property
    def black(self) -> wire.Pin:
        return wire.Pin(self, 1)